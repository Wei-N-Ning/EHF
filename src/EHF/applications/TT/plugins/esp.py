from EHF.libs import ehfgraphics
from EHF.plugins import base
from EHF.applications.TT import datastruct
from EHF.libs import ehfmaths
from EHF.libs.ehfmaths import functions as ehfmaths_functions
from EHF.libs.ehfui import widgets


class PrototypeEspPlugin(base.BasePerFrameDrawingPlugin):
    """
    Experimental esp, drawing with static data
    """
    def initialise(self):
        self.colorTeammate = self._appAttr["EnvInfo"].boxLineColorAlt
        self.colorEnemy    = self._appAttr["EnvInfo"].boxLineColor
        self.lineWidth = self._appAttr["EnvInfo"].boxLineWidth
        self.screenCenterX = 0
        self.screenCenterY = 0
        self.appVars = None
        self.appInfo = None
        self.hasDelayInitialised = False
        
        self.miniMap = None
        
    def delayedInit(self):
        if not self.hasDelayInitialised:
            self.miniMap = widgets.SimpleMiniMap( 
                 # location control
                 centerX=170, centerY=130, boundaryX=160, boundaryY=120,
                 # color/drawing style
                 borderWidth=3, lineWidth=3, selfColor=0xFF00FF00, teamColor=0xFF1111FF, enemyColor=0xFFFF1111, boundaryColor=0xFFFF1111,
                 # size/scale control
                 scale=2, spotSize=3,
                 # other attributes
                 )
            self.hasDelayInitialised = True
            
    def _run(self):
        # delayed init
        self.delayedInit()

        self.miniMap.drawBoundary(self.getLine())
        self.miniMap.drawSelf(self.getLine())
        
