"""
defines the window frame plugin for all the win gui applications
"""
import threading
import time
import sys

from EHF.plugins import base



import logging
logging.basicConfig()
logger = logging.getLogger(__name__)



class WindowCreateWindowFramePlugin(base.BasePreExecutionPlugin):
    """
    """
    requirements = []
    contributions = []
    
    def _run(self):
        """
        """
        pass


class WindowBeginPaintPlugin(base.BasePerFramePlugin):
    """
    schedule a begin paint event for every frame
    """
    requirements = [ "WindowFrame" ]
    contributions = []
    
    def _run(self):
        """
        schedule the begin paint event; calling WindowFrame.BeginPaint()
        """
        self._appAttr["WindowFrame"].BeginPaint()



class WindowEndPaintPlugin(base.BasePerFramePlugin):
    """
    schedule a end paint event for every frame
    """
    requirements = [ "WindowFrame" ]
    contributions = []
    
    def _run(self):
        """
        schedule the end paint event; calling WindowFrame.EndPaint()
        """
        self._appAttr["WindowFrame"].EndPaint()

    

class DeleteWindowFramePlugin(base.BasePostExecutionPlugin):
    """
    Free the window resources, stop the window thread
    """
    requirements = [ "AppInfo", "WindowFrame" ]
    contributions = []

    def _run(self):
        """
        call release_d3d method from WindowFrame
        """
        logger.debug("Preparing to free d3d devices...")
        self._appAttr["WindowFrame"].release_d3d()
        logger.debug("Released d3d")
        
    def _push(self):
        self._appAttr["exit"] = True
        self._appAttr["WindowThread"].join()
        self._appAttr["WindowThread"] = None
        logger.debug("Delete reference to WindowThread")
        self._appAttr["WindowFrame"] = None
        logger.debug("Delete reference to WindowFrameHandle")