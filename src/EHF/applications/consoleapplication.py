import threading
import time
import sys

from EHF.core import application
from EHF.core import entity

from EHF.libs.ehfmemory import reader
from EHF.libs import ehfprocess

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class ConsoleApplication(application.BaseApplication):
    
    """
    The standard interface of console application.
    
    It implements a stdin-based interaction that allows the user to type in commands
    that control the execution.
    
    The execution model consists of PreExection, PerFrameExecution and PostExecution
    """
    
    def initAttributes(self):
        self._attributes["AppInfo"] = entity.AppInfo()
        self._attributes["EnvInfo"] = entity.EnvInfo()
        self._attributes["ProcessHelper"] = ehfprocess.ProcessHelper()
        self._attributes["flag_processReady"] = False
        self._attributes["MemoryReader"] = None
        
        self._initAppInfo()
        self._initEnvInfo()
        self._initProcess()
    
    def _initProcess(self):
        self._attributes["ProcessHelper"].findWindowByClass(self._attributes["AppInfo"].targetAppWindowClass)
        if not (self._attributes["ProcessHelper"].pid and\
                self._attributes["ProcessHelper"].tid and\
                self._attributes["ProcessHelper"].hwnd):
            logger.error("Can not find target process. Exit.")
            sys.exit(1)
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
    
    def _initAppInfo(self):
        """
        to be implemented per-application 
        """
        pass
    
    def _initEnvInfo(self):
        """
        to be implemented per-application or leave it as default
        """
        pass

    def _dataPass(self):
        """
        the execution of all the data-related per-frame functions, 
        read process memory, populate/parse data structure etc etc
        
        to be implemented in the derived classes
        """
        for _plugin in self._pluginRegistry[application.PerFrameDataPluginType]:
            _plugin.run()

    def _preExecution(self):
        """
        executed before the main loop
        
        calls all the PreExecutionPlugins
        """
        for _plugin in self._pluginRegistry[application.PreExecutionPluginType]:
            _plugin.run()
  
    def _execute(self):
        self._preExecution()
        tickCount = 0
        while not self._debugFlag or \
              (self._debugFlag and tickCount) or \
              self._terminate:
            self._dataPass()
            self._cleanUp()
            time.sleep(1 / self._attributes["FPS"])
            
    def execute(self):
        logger.info("Start _execute()....")
        self._execute()
        logger.info("Application finishes execution(), going to clean up")
        self.cleanUp()
    
    def _cleanUp(self):
        pass
    
    def cleanUp(self):
        pass
    
    def release(self):
        pass