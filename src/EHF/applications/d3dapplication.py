import threading
import time
import win32gui
import sys

from EHF.libs import ehfgraphics as graphics

from EHF.core import application
from EHF.applications import d3dwindowframe
from EHF.core import entity

from EHF.libs.ehfmemory import reader
from EHF.libs import ehfprocess

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class D3DApplication(application.BaseApplication):
    
    """
    The standard interface of a direct3d application. 
    The core of this class is the execution model, which consists of:
    
    * PreExecution, 
      run only once after the execution starts, mostly to prepare the environment 
      for the per-frame execution or to provide the preliminary data... (such the job
      of a memory scanner) 
    * PerFrameExecution, consists of:
      a series of routines preparing for the drawing (such as read memory etc)
      a series of routines draw stuff on the window, bracketed by BeginPaint() and EndPaint() methods.
    * PostExecution,
      run after the iteration of the per-frame execution finishes, mostly some clean up jobs
    
    Shared properties (along with _attributes)
    * appinfo: app name, window clas name ......
    * envinfo: drawing properties, line color ...... 
    """

    def initAttributes(self):
        self._attributes["AppInfo"] = None
        self._attributes["EnvInfo"] = None
        self._attributes["WindowFrame"] = None
        self._attributes["WindowThread"] = None
        self._attributes["ProcessHelper"] = ehfprocess.ProcessHelper()
        self._attributes["flag_processReady"] = False
        self._attributes["MemoryReader"] = None
        
        self._initThreadLock()
        self._initAppInfo()
        self._initEnvInfo()
        self._initProcess()
    
    def _initThreadLock(self):
        self.lock = threading.Lock()
        
    def _initProcess(self):
        if self.isPrototypeApplication:
            self.__initPrototypeProcessAttributes()
        else:
            self._attributes["ProcessHelper"].findWindowByClass(self._attributes["AppInfo"].targetAppWindowClass)
            if not (self._attributes["ProcessHelper"].pid and\
                    self._attributes["ProcessHelper"].tid and\
                    self._attributes["ProcessHelper"].hwnd):
                logger.error("Can not find target process. Exit.")
                sys.exit(1)
            self.__initProcessAttributes()
            self.__printProcessAttribute()
        
    def __initPrototypeProcessAttributes(self):
        """
        to "hardcode" these window related attributes....
        really bad design but won't break the existing tools
        
        these hardcoded attributes are defined in the AppInfo class, 
        nothing needs to be done here....
        """
        pass
        
    def __initProcessAttributes(self):
        self._attributes["ProcessHelper"].populateWindowRect()
        self._attributes["ProcessHelper"].openProcess()
        
        self._attributes["AppInfo"].bboxLeft = self._attributes["ProcessHelper"].windowRect.left
        self._attributes["AppInfo"].bboxRight = self._attributes["ProcessHelper"].windowRect.right
        self._attributes["AppInfo"].bboxTop = self._attributes["ProcessHelper"].windowRect.top
        self._attributes["AppInfo"].bboxBottom = self._attributes["ProcessHelper"].windowRect.bottom
        self._attributes["AppInfo"].resolutionX = self._attributes["ProcessHelper"].clientRect.right - self._attributes["ProcessHelper"].clientRect.left
        self._attributes["AppInfo"].resolutionY = self._attributes["ProcessHelper"].clientRect.bottom - self._attributes["ProcessHelper"].clientRect.top
        self._attributes["AppInfo"].centerX = self._attributes["AppInfo"].resolutionX / 2
        self._attributes["AppInfo"].centerY = self._attributes["AppInfo"].resolutionY / 2
        self._attributes["AppInfo"].originX = self._attributes["ProcessHelper"].origPoint.x
        self._attributes["AppInfo"].originY = self._attributes["ProcessHelper"].origPoint.y
        self._attributes["MemoryReader"] = reader.MemoryReader(self._attributes["ProcessHelper"].hProcess)
        
    def __printProcessAttribute(self):
        logger.info("bboxLeft: %d" % self._attributes["AppInfo"].bboxLeft)
        logger.info("bboxRight: %d" % self._attributes["AppInfo"].bboxRight)
        logger.info("bboxTop: %d" % self._attributes["AppInfo"].bboxTop)
        logger.info("bboxBottom: %d" % self._attributes["AppInfo"].bboxBottom)
        logger.info("resolutionX: %d" % self._attributes["AppInfo"].resolutionX)
        logger.info("resolutionY: %d" % self._attributes["AppInfo"].resolutionY)
        logger.info("centerX: %d" % self._attributes["AppInfo"].centerX)
        logger.info("centerY: %d" % self._attributes["AppInfo"].centerY)
        logger.info("originX: %d" % self._attributes["AppInfo"].originX)
        logger.info("originY: %d" % self._attributes["AppInfo"].originY)
        logger.info("hProcess: %d" % self._attributes["ProcessHelper"].hProcess)
    
    def _initAppInfo(self):
        """
        to be implemented per-application, to initialize the application-based AppInfo object
        """
        pass
    
    def _initEnvInfo(self):
        """
        to be implemented per-application or leave it as default, to initialize the application-base
        EnvInfo object
        """
        pass
    
    def _initWindowFrame(self):
        self._attributes["WindowFrame"] = d3dwindowframe.WindowFrame(self._attributes["AppInfo"])
        logger.info("...instantiated window frame")
        self._attributes["WindowFrame"].createWindow()
        logger.info("...done createWindow()")
        logger.info("...running showWindow()")
        self._attributes["WindowFrame"].showWindow()
        
    def windowThread(self):
        self._initWindowFrame()
        win32gui.PumpMessages()
    
    def _dataPass(self):
        """
        the execution of all the data-related per-frame functions, 
        read process memory, populate/parse data structure etc etc
        """
        for _plugin in self._pluginRegistry[application.PerFrameDataPluginType]:
            _plugin.run()
    
    def _drawingPass(self):
        """
        the execution of all the drawing-related per-frame functions,
        draw lines, boxes, burn-in fonts etc etc
        """
        for _plugin in self._pluginRegistry[application.PerFrameDrawingPluginType]:
            _plugin.run()
    
    def _preExecution(self):
        """
        executed before the main loop, calling all the PreExecutionPlugins
        """
        for _plugin in self._pluginRegistry[application.PreExecutionPluginType]:
            _plugin.run()
    
    def _execute(self):
        """
        main per-frame execution loop
        """
        while not self._terminate:
            
            # data pass 
            self._dataPass()
            
            # drawing pass
            self._attributes["WindowFrame"].BeginPaint()
            self._drawingPass()
            self._attributes["WindowFrame"].EndPaint()
            
            # clean up
            self._cleanUp()
            
            time.sleep(1 / self._attributes["FPS"])
            
    def execute(self):
        """
        VERY IMPORTANT: 
        Scanner (a pre-execution plugin) will access to the hProcess
        attribute. It must completely finish before the window thread
        starts, otherwise will result in a racing condition and CRASH!!!!
        
        ALSO VERY IMPORTANT:
        worth to write the document the order of create window / d3d device
        
        main thread   : <create window thread>                                          wait till created, initialize d3d device
        
                            window thread:     create window, show window, pump message 
        
        """

        # --------pre-execution--------
        self._preExecution()
        
        # -------start window thread-------
        self._attributes["WindowThread"] = threading.Thread(target=self.windowThread)
        self._attributes["WindowThread"].start()
        
        windowReady = False
        while not windowReady:
            try:
                self.lock.acquire()
                if self._attributes["WindowFrame"] and self._attributes["WindowFrame"].hwnd:
                    windowReady = True
            finally:
                self.lock.release()
            time.sleep(0.1)
        
        self._attributes["WindowFrame"].init_d3d()
        logger.info("...done init_d3d()")
        
        while not ( self._attributes["WindowFrame"] and\
                    self._attributes["WindowFrame"].device and\
                    getattr(self._attributes["WindowFrame"].device, "Clear") ):
            logger.info("\n\n......Waiting for WindowFrame\n\n")
            time.sleep(0.1)
            
        # -------main execution loop-------
        logger.info("Start _execute()....")
        self._execute()
        logger.info("Application finishes execution(), going to clean up")
        
        # ---------clean up----------
        self.cleanUp()
    
    def _cleanUp(self):
        """
        The per-frame cleanUp routine
        
        There're also per-frame-post-execution plugin template class that can do exactly the
        same thing, but the general rule of the thumb is: less plugin the better, 
        And for the per-frame cleanUp it just needs to flush the display list, doesn't
        worth the create the plugin anyway....
        """
        self._attributes["AppInfo"].displayTextList = []
    
    def cleanUp(self):
        """
        The post-execution cleanUp routine...
        It should call the release_d3d() function.
        """
        self._attributes["WindowFrame"].release_d3d()
    
    def release(self):
        self._attributes["WindowFrame"].release_d3d()