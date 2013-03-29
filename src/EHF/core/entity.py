"""
entity module holds the brick-building objects required by application/plugin or library functions
"""

from EHF.libs import ehfmaths

class AppInfo(object):
    """
    a simple class holding the application information
    
    appName: nice little name for the app
    bx, by: bounding box x, y
    rx, ry: resolution x, y
    isDryRun: set True for test only
    isProfiling: set True for profiling
    
    """
    def __init__(self):
        
        self.appName = ''
        self.hProcess = 0x0
        
        self.isDryRun = True
        self.noRun = False
        self.isProfiling = False
        self.exit = False
        
        self.bboxLeft = 0
        self.bboxRight = 0
        self.bboxTop = 0
        self.bboxBottom = 0

        self.resolutionX = 0
        self.resolutionY = 0
        
        self.centerX = 0
        self.centerY = 0
        
        self.originX = 0
        self.originY = 0
        
        self.time = 0
        self.ticks = 0
        self.targetAppName = ''
        self.targetAppWindowClass = ''
        
        # these two attributes are VERY important!
        # they define the memory scan range for the initial reading
        # for example for COD series, the range would typically be 0x00401000 - 0x00700000
        self.targetMemStart = 0x0
        self.targetMemSize = 0x0
        
        # display text list
        self.displayTextList = []
        self.titleTextList = []
        
        # primary variable hash table
        # it stores the static address, array addres etc.
        self.primaryVars = {}
        
        # it is the main variable repository, holding all kinds of
        # data interested to the plugins
        # it must match the plugin requirements, though it's not validated
        self.vars = {}
        
        # stores the name-mapped key or mouse state
        self.keyMouseInputState = {}
        
        self.override()
    
    def override(self):
        """
        for sub-classes to override the attributes
        """
        pass
    
        
class EnvInfo(object):
    """
    a simple class holding all the app-global configurations.
    
    it's different from global config which affects all the application,
    here it only affects one application and others can have their own
    environment variables
    """
    def __init__(self):
        self.crossHairLineColor = 0xFFFF1111
        self.crossHairLineWidth = 2
        self.crossHairSize = 6
        self.boxLineColor = 0xFFFF1111
        self.boxLineColorAlt = 0xFF1111FF
        self.boxLineWidth = 2
        self.fontColor = 0xFFFF1111
        self.fontWidth = 40
        self.fontHeight = 10
        self.fontMargin = 5
        
        self.override()
        
    def override(self):
        """
        for sub-classes to override the attributes
        """
        pass
        

class KeyMouse(object):
    def __init__(self, name, id, type, state):
        self.name = name
        self.id = id
        self.type = type
        self.state = state
        
        