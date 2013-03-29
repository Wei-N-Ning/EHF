"""
Plugins are the main components of every EHF application. They are the workers that do the actual work.
The application is merely a place holder (or data holder) and a scheduler (so it's pretty dumb in scheduling).

Based on the type of the plugin, there're mainly two group of plugins: the one executed per-frame and those
executed on the application scope, upon application startup or cleanup. 

Plugin reads data from application and may pass data back to application.
"""

class BasePlugin(object):
    """
    define the basic interface of the plugin
    """
    type = ""
    uid = 0x0
    requirements = []
    contributions = []
    
    def __init__(self, application=None):
        self._application = application
        self._appAttr = application.getAttributeRepo()
        self.initialise()
    
    def initialise(self):
        pass
    
    def getType(self):
        return self.type
    
    def getAppAttr(self, attr=""):
        return getattr(self._appAttr, attr, None)
    
    def setAppAttr(self, attr="", value=None):
        setattr(self._appAttr, attr, value)
    
    def _push(self):
        pass
    
    def _pull(self):
        pass
    
    def _run(self):
        """
        run() method will execute the _pull(), _run(), _push() methods,
        implement these methods to your need
        """
        pass
    
    def run(self):
        self._pull()
        self._run()
        self._push()
        
        
        

class BasePostExecutionPlugin(BasePlugin):
    """
    To run right after the main application loop exits.
    It's responsible for cleanup tasks
    """
    type = "PostExecution"
    uid = 0x1
    
    
    
class BasePerFrameDataPlugin(BasePlugin):
    """
    To run per-frame in the main application loop.
    """
    type = "PerFrameData"
    uid = 0x2

class BasePerFrameDrawingPlugin(BasePlugin):
    type = "PerFrameDrawing"
    uid = 0x4
    
    def getLine(self):
        return self._appAttr["WindowFrame"].line
    
    def getFont(self):
        return self._appAttr["WindowFrame"].font
    
    def getclw(self):
        return self._appAttr["EnvInfo"].crossHairLineWidth
    
    def getclc(self):
        return self._appAttr["EnvInfo"].crossHairLineColor
    
    def getcs(self):
        return self._appAttr["EnvInfo"].crossHairSize
    
    def getblw(self):
        return self._appAttr["EnvInfo"].boxLineWidth
    
    def getblc(self):
        return self._appAttr["EnvInfo"].boxLineColor
    
    def getblca(self):
        return self._appAttr["EnvInfo"].boxLineColorAlt
    
class BasePreExecutionPlugin(BasePlugin):
    """
    To run right before the main application loop starts.
    
    It's responsible for set up the application environment, populating the 
    essential attributes etc.
    
    Every application must have at least one PreExecutionPlugin.
    """
    type = "PreExecution"
    uid = 0x3