from EHF.libs import ehfgraphics
from EHF.plugins import base
from EHF.applications.MOHW import datastruct
from EHF.libs import ehfmaths
from EHF.libs.ehfmaths import functions as ehfmaths_functions
from EHF.libs.ehfui import widgets


class EspPlugin(base.BasePerFrameDrawingPlugin):
    """
    Draw the esp
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
            self.appVars = self._appAttr["AppInfo"].vars
            self.appInfo = self._appAttr["AppInfo"]
            self.screenCenterX = self.appInfo.centerX
            self.screenCenterY = self.appInfo.centerY
            self.hasDelayInitialised = True
            
    def _run(self):
        # delayed init
        self.delayedInit()
        worldTransform = ehfmaths_functions.getIdMatrix()
        viewTransform = ehfmaths_functions.getViewMatrix(
                                                         self.appVars["upVec"], 
                                                         self.appVars["rightVec"], 
                                                         self.appVars["forwardVec"], 
                                                         self.appVars["viewOrigin"]
                                                         )
        
        if not self.miniMap:
            self.miniMap = widgets.SimpleMiniMap( 
                 # location control
                 centerX=200, centerY=200, boundaryX=160, boundaryY=160,
                 # color/drawing style
                 borderWidth=3, lineWidth=3, selfColor=0xFF00FF00, teamColor=0xFF1111FF, enemyColor=0xFFFF1111, boundaryColor=0xFFFF1111,
                 # size/scale control
                 scale=2, spotSize=3,
                 # other attributes
                 vecForward=self.appVars["forwardVec"]
                 )
        else:
            self.miniMap.setVecForward(self.appVars["forwardVec"])
            self.miniMap.setViewAxisZ(self.appVars["forwardVec"])

        self.miniMap.drawBoundary(self.getLine())
        self.miniMap.drawSelf(self.getLine())
        
        projectionTransform = ehfmaths_functions.getProjectionMatrix(
                                                                     self.appVars["zn"], 
                                                                     self.appVars["zf"], 
                                                                     self.appVars["fov_x"], 
                                                                     self.appVars["fov_y"]
                                                                     )

        # loop through simple player objects
        for player in self.appVars["players"]:
            # don't draw "self"
            if player.address == self.appVars["localPlayerAddress"]:
                continue
            
            if not self._validatePlayer(player):
                continue
            _color = self.colorTeammate if player.teamId == self.appVars["localPlayerTeamId"] \
                                        else self.colorEnemy
            pos4 = player.position.toPointVector4()
            _posV = pos4.multToMat(worldTransform).multToMat(viewTransform)
            _posVP = _posV.multToMat(projectionTransform)
            _posV.x = _posV.x * -1
            self.miniMap.drawPlayer(self.getLine(), _posV, player.teamId == self.appVars["localPlayerTeamId"])

            if abs(_posVP.w) < 0.001:
                continue
            if _posVP.z > 0:
                continue
            x = self.screenCenterX*(1+_posVP.x/_posVP.w)
            y = self.screenCenterY*(1+_posVP.y/_posVP.w)
            ehfgraphics.drawSpot(self.getLine(),
                                 x,
                                 y, 
                                 _color,
                                 size=4)
            
            
    def _validatePlayer(self, player):
        if player.address:
            return True
        else:
            return False
    