"""
This module contains the data structures for all the applications

Application can define their own data structure and overrides this global data structure definition
"""
from win32types import *


class COORD(Structure):
    """
    simple coordinate struct
    """
    _fields_ = [ ("x", c_float),
                 ("y", c_float) ]


class RECT(Structure):
    _fields_ = [ ("left", c_int),
                 ("top", c_int),
                 ("right", c_int),
                 ("bottom", c_int) ]
    
    
class POINT(Structure):
    """
    this is stupid.... fucking Microsoft....
    """
    _fields_ = [ ("x", c_int),
                 ("y", c_int) ]
    

class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pt', POINT)]


class STR16(Structure):
    _fields_ = [ ("str", c_char * 16)]
    
    
class STR32(Structure):
    _fields_ = [ ("str", c_char * 32)]


class STR64(Structure):
    _fields_ = [ ("str", c_char * 64)]


class STR256(Structure):
    _fields_ = [ ("str", c_byte * 256)]


class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_longlong),
                ('hIcon', c_longlong),
                ('hCursor', c_longlong),
                ('hbrBackground', c_longlong),
                ('lpszMenuName', c_char_p),
                ('lpszClassName', c_char_p)]
    

class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', c_int),
                ('fErase', c_int),
                ('rcPaint', RECT),
                ('fRestore', c_int),
                ('fIncUpdate', c_int),
                ('rgbReserved', c_char * 32)]


class MARGINS(Structure):
    _fields_ = [ ("cxLeftWidth", c_int),
                 ("cxRightWidth", c_int),
                 ("cyTopHeight", c_int),
                 ("cyBottomHeight", c_int),] 
