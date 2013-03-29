import win32gui, win32con, win32api 

from directx.d3d import IDirect3D9, IDirect3DDevice9
from directx.d3dx import d3dxdll, TestHR, ID3DXFont, ID3DXLine, ID3DXSprite
import directx.types as d3dtypes

from ctypes import windll
from ctypes import WinError
from ctypes import oledll
from ctypes import byref

from EHF.core import datastruct
from EHF.core.win32types import *
from EHF.core.fonts import *

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

kernel32 = windll.kernel32


class D3DWindowFrameError(Exception):
    pass


class D3DRenderState(object):
    """
    A simple structure holding the d3d render state constants
    """
    D3DRS_ZENABLE                      = 7
    D3DRS_LIGHTING                     = 137
    D3DRS_CULLMODE                     = 22



class ExtendedWindowStyles(object):
    """
    A simple structure holding the WS_EX_* constants
    
    original definition:
    http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    """
    def __init__(self):
        self.WS_EX_ACCEPTFILES = 0x00000010
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_CLIENTEDGE = 0x00000200
        self.WS_EX_CONTEXTHELP = 0x00000400
        self.WS_EX_CONTROLPARENT = 0x00010000
        self.WS_EX_DLGMODALFRAME = 0x00000001
        self.WS_EX_LAYOUTRTL = 0x00400000
        self.WS_EX_LEFT = 0x00000000
        self.WS_EX_LEFTSCROLLBAR = 0x00004000
        self.WS_EX_LTRREADING = 0x00000000
        self.WS_EX_MDICHILD = 0x00000040
        self.WS_EX_NOACTIVATE = 0x08000000
        self.WS_EX_NOINHERITLAYOUT = 0x00100000
        self.WS_EX_NOPARENTNOTIFY = 0x00000004
        self.WS_EX_RIGHT = 0x00001000
        self.WS_EX_RIGHTSCROLLBAR = 0x00000000
        self.WS_EX_RTLREADING = 0x00002000
        self.WS_EX_STATICEDGE = 0x00020000
        self.WS_EX_TOOLWINDOW = 0x00000080
        
        # the following four are required for transparent overlay (windows Areo)
        # only the WS_EX_TOPMOST is required for non-overlay window
        self.WS_EX_TOPMOST = 0x00000008 
        self.WS_EX_TRANSPARENT = 0x00000020
        self.WS_EX_LAYERED = 0x00080000
        self.WS_EX_COMPOSITED = 0x02000000
        
        self.WS_POPUP = 0x80000000
        
        self.WS_EX_WINDOWEDGE = 0x00000100
        self.WS_EX_OVERLAPPEDWINDOW = self.WS_EX_WINDOWEDGE | self.WS_EX_CLIENTEDGE
        self.WS_EX_PALETTEWINDOW = self.WS_EX_WINDOWEDGE | self.WS_EX_TOOLWINDOW | self.WS_EX_TOPMOST
    
    def getAeroStyle(self):
        return self.WS_EX_TOPMOST | self.WS_EX_TRANSPARENT | self.WS_EX_LAYERED | self.WS_EX_COMPOSITED
    
    def getStdStyle(self):
        return self.WS_EX_TOPMOST | self.WS_EX_CLIENTEDGE
    
    

def wndProc(hwnd, message, wParam, lParam): 
    if message == 2:                    #WM_DESTROY        
        windll.user32.PostQuitMessage(0)
        return 0                 
    else:
        return windll.user32.DefWindowProcA(c_int(hwnd), 
                                            c_int(message), 
                                            c_int(wParam), 
                                            c_int(lParam))


WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)
    

class WindowFrame(object):
    """
    This is the window class for all the application that runs in a win7 aero window.
    """
    def __init__(self, appInfo):
        """
        appInfo is a data structure passed in by the initialization plugin from the application 
        
        [IMPORTANT]
        even though python dictionary is thread safe, python object is NOT!!
        do not keep a reference to the appInfo object in this window thread, 
        it's being constantly modified by the data thread!!!!!
        
        NOTE:
        There are two different way of drawing the window: "attached mode" and "standalone mode",
        "attach mode" means the window will use Areo transparent window feature and draw the window
        exactly on top of the target window. This mode requires the special combination of WS_EX
        flags and also the target window's coords (via the appInfo)
        "standalone mode" means the window will be drawn in a standard win style and at arbitary
        location (specified in the appInfo)
        """
        self.appName = appInfo.appName
        self.isProfiling = appInfo.isProfiling
        self.isDryRun = appInfo.isDryRun
        self.originX = appInfo.originX
        self.originY = appInfo.originY
        self.resolutionX = appInfo.resolutionX
        self.resolutionY = appInfo.resolutionY
        
        self.hwnd = None
        self.device = None
        
        self.extendedWindowStyles = ExtendedWindowStyles()
        
    def createWindow(self):
        # this is to be called by a specific thread that will be the owner
        hInstance = kernel32.GetModuleHandleA(None)
        wndClass                = datastruct.WNDCLASS()
        wndClass.style          = 0
        wndClass.lpfnWndProc    = WNDPROC(wndProc)
        wndClass.hInstance      = hInstance
        wndClass.hIcon          = windll.user32.LoadIconA(0, 32512)     # 32512 = IDI_APPLICATION
        wndClass.hCursor        = windll.user32.LoadCursorA(0, 32512)   # 32512 = IDC_ARROW
        wndClass.hbrBackground  = 0
        wndClass.lpszClassName  = str(self.appName)                 # not Unicode
        wndClass.lpszMenuName   = None
        
        if not windll.user32.RegisterClassA(byref(wndClass)):
            raise WinError()
        
        window_style_flag = 0
        if self.isDryRun:
            window_style_flag = self.extendedWindowStyles.getStdStyle()
        else:
            window_style_flag = self.extendedWindowStyles.getAeroStyle()
        
        logger.debug("calling CreateWindowExA() with:\n"\
                     "window style flag: %s\n"\
                     "self.appName: %s\n"\
                     "self.extendedWindowStyles.WS_POPUP: %s\n"\
                     "self.originX: %s\n"\
                     "self.originY: %s\n"\
                     "self.resolutionX: %s\n"\
                     "self.resolutionY: %s\n" % (window_style_flag, self.appName, self.extendedWindowStyles.WS_POPUP,
                                                 self.originX, self.originY, self.resolutionX, self.resolutionY))
        
        hwnd = windll.user32.CreateWindowExA(
            window_style_flag,
            self.appName,
            self.appName,
            self.extendedWindowStyles.WS_POPUP,
            self.originX,
            self.originY,
            self.resolutionX,
            self.resolutionY,
            None,
            None,
            hInstance,
            None)
        
        if not hwnd:
            raise D3DWindowFrameError, "Failed to create hwnd!!"
        else:
            logger.debug("+ Successfully created hwnd: %s" % hwnd)
        
        # make a transparent window
        if not self.isDryRun:
            oledll.Dwmapi.DwmExtendFrameIntoClientArea(hwnd, 
                                                       byref(datastruct.MARGINS(-1, -1, -1, -1)))
            compo = c_int()
            oledll.Dwmapi.DwmIsCompositionEnabled(byref(compo))
            if not compo:
                raise Exception("Composition is not activated")
        self.hwnd = hwnd


    def showWindow(self):            
        win32gui.ShowWindow(self.hwnd, 1)      # SW_SHOWNORMAL = 1
        win32gui.UpdateWindow(self.hwnd)
    

    def init_d3d(self):
        address = windll.d3d9.Direct3DCreate9(UINT(d3dtypes.D3D_SDK_VERSION))
        
        params = d3dtypes.D3DPRESENT_PARAMETERS()
        params.Windowed            = True
        params.SwapEffect          = d3dtypes.D3DSWAPEFFECT.DISCARD  # Required for multi sampling
        params.BackBufferFormat    = d3dtypes.D3DFORMAT.A8R8G8B8     # Back buffer format with alpha channel
        params.MultiSampleType     = 0                      # D3DMULTISAMPLE_NONE
        
        self.d3d = POINTER(IDirect3D9)(address)
        self.device = POINTER(IDirect3DDevice9)()
        
        if not self.isDryRun:
            self.d3d.CreateDevice(0, d3dtypes.D3DDEVTYPE.HAL, self.hwnd, d3dtypes.D3DCREATE.HARDWARE_VERTEXPROCESSING, byref(params), byref(self.device))
        else:
            self.d3d.CreateDevice(0, d3dtypes.D3DDEVTYPE.HAL, self.hwnd, d3dtypes.D3DCREATE.HARDWARE_VERTEXPROCESSING, byref(params), byref(self.device))
        
        self.device.SetRenderState(D3DRenderState.D3DRS_ZENABLE,
                                   False)
        self.device.SetRenderState(D3DRenderState.D3DRS_LIGHTING, 
                                   False)
        self.device.SetRenderState(D3DRenderState.D3DRS_CULLMODE, 
                                   d3dtypes.D3DCULL.NONE)
        
        # common objects        
        d3dxdll.D3DXCreateFontW.restype = TestHR
        self.font = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW(self.device, 
                                PLAYER_NAME_SIZE, 
                                0, 
                                PLAYER_NAME_WEIGHT, 
                                1, 0, 0, 0, 0, 0, 
                                LPCWSTR(unicode(PLAYER_NAME_FONT)), 
                                byref(self.font)) #@UndefinedVariable
        self.status_font = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW(self.device, 
                                14, 0, 400, 1, 0, 0, 0, 0, 0, 
                                LPCWSTR(u"Arial"), 
                                byref(self.status_font)) #@UndefinedVariable
        self.killstreak_font = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW(self.device, 
                                KILLSTREAK_FONT_SIZE, 
                                0, 
                                KILLSTREAK_FONT_WEIGHT, 
                                1, 0, 0, 0, 0, 0, 
                                LPCWSTR(unicode(KILLSTREAK_FONT_NAME)), 
                                byref(self.killstreak_font)) #@UndefinedVariable
        self.rage_font = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW(self.device, 
                                RAGE_FONT_SIZE, 
                                0, 
                                RAGE_FONT_WEIGHT, 
                                1, 0, 0, 0, 0, 0, 
                                LPCWSTR(unicode(RAGE_FONT_NAME)), 
                                byref(self.rage_font)) #@UndefinedVariable
        self.ammo_font = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW(self.device, 
                                AMMO_COUNTER_FONT_SIZE, 
                                0, 
                                AMMO_COUNTER_FONT_WEIGHT, 
                                1, 0, 0, 0, 0, 0, 
                                LPCWSTR(unicode(AMMO_COUNTER_FONT_NAME)), 
                                byref(self.ammo_font)) #@UndefinedVariable
        self.c4_font = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW(self.device, 
                                C4AUTOFIRE_FONT_SIZE, 
                                0, 
                                C4AUTOFIRE_FONT_WEIGHT, 
                                1, 0, 0, 0, 0, 0, 
                                LPCWSTR(unicode(C4AUTOFIRE_FONT_NAME)), 
                                byref(self.c4_font)) #@UndefinedVariable
        self.cooking = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW(self.device, 
                                GRENADECOOKING_FONT_SIZE, 
                                0, 
                                GRENADECOOKING_FONT_WEIGHT, 
                                1, 0, 0, 0, 0, 0, 
                                LPCWSTR(unicode(GRENADECOOKING_FONT_NAME)), 
                                byref(self.cooking)) #@UndefinedVariable
        
        self.line = POINTER(ID3DXLine)()
        d3dxdll.D3DXCreateLine.restype = TestHR
        d3dxdll.D3DXCreateLine(self.device, byref(self.line)) #@UndefinedVariable
        
        self.line.SetWidth(5)
        self.line.SetPattern(0xFFFFFFFF)
        self.line.SetAntialias(True)
        
        self.sprite = POINTER(ID3DXSprite)()
        d3dxdll.D3DXCreateSprite(self.device, 
                                 byref(self.sprite)) #@UndefinedVariable
        
        
    def release_d3d(self):
        if not self.line is None:               self.line.Release()
        if not self.status_font is None:        self.status_font.Release()
        if not self.killstreak_font is None:    self.killstreak_font.Release()
        if not self.rage_font is None:          self.rage_font.Release()
        if not self.ammo_font is None:          self.ammo_font.Release()
        if not self.font is None:               self.font.Release()
        if not self.device is None:             self.device.Release()
        if not self.d3d is None:                self.d3d.Release()
        if not self.sprite is None:             self.sprite.Release()
        
        
    def BeginPaint(self):
        """
        TODO: update the window position if target window is moved
        if self.ticks % 10 == 0:            # check not too often
            windll.user32.MoveWindow(self.hwnd, 
                                     self.boundingX, 
                                     self.boundingY,
                                     self.resolutionX, 
                                     self.resolutionY, 
                                     False)
        """
        self.device.Clear(0, 
                          None, 
                          d3dtypes.D3DCLEAR.TARGET, 
                          0x00000000, 1, 0)
        self.device.BeginScene()        
    
    
    def EndPaint(self):
        self.device.EndScene()
        if not self.isProfiling:
            self.device.Present(None, None, self.hwnd, None)    