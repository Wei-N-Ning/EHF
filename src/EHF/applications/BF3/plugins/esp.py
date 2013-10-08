
from EHF.libs import ehfgraphics
from EHF.plugins import base
from EHF.applications.BF3 import datastruct
from EHF.libs import ehfmaths
from EHF.libs.ehfmaths import functions as ehfmaths_functions
from EHF.libs.ehfui import widgets

#it is bad....
SPEED = 200.0
GRAVITY = 9.81


def naiveGetBulletDrop(distance, deltaY, gravity, velocity):
    try:
        sinAimA = deltaY/distance
    except:
        return 0.0
    # this is wrong
    bulletTravelTime = distance/SPEED
    # this is inaccurate, it does not account for the change of sinAimA which affects the 
    # vertical bullet speed
    bulletTravelDistanceY = SPEED * sinAimA * bulletTravelTime - GRAVITY/2.0 * bulletTravelTime**2
    return deltaY - bulletTravelDistanceY

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
        
        # figure out the time interval
        worldTransform = ehfmaths_functions.getIdMatrix()
        viewTransform = ehfmaths_functions.getViewMatrix(
                                                         self.appVars["upVec"], 
                                                         self.appVars["rightVec"], 
                                                         self.appVars["forwardVec"], 
                                                         self.appVars["viewOrigin"]
                                                         )
        viewOrigin = self.appVars["viewOrigin"].toPointVector4()
        
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
        
        hintColor = 0xFFFF11FF
        
        # loop through simple player objects
        for player in self.appVars["players"]:
            # don't draw "self"
            if player.address == self.appVars["localPlayerAddress"]:
                continue
            
            # skip team players
            if player.teamId == self.appVars["localPlayerTeamId"]:
                continue
                
            if not self._validatePlayer(player):
                continue
            
            _color = self.colorTeammate if player.teamId == self.appVars["localPlayerTeamId"] \
                                        else self.colorEnemy
            pos4 = player.position.toPointVector4()
            pos4TankAimAssist = player.position.toPointVector4()
            
            distant = (pos4 - viewOrigin)._length()
            deltaY = pos4.y - viewOrigin.y
            
            _posV = pos4.multToMat(worldTransform).multToMat(viewTransform)
            _posVP = _posV.multToMat(projectionTransform)
            _posV.x *= -1
            
            # ----------------get bullet drop
            aimCompensationY = naiveGetBulletDrop(distant, deltaY, GRAVITY, SPEED)
            # ----------------done getting bullet drop
            
            pos4TankAimAssist.y += aimCompensationY 
            posVTankAimAssist = pos4TankAimAssist.multToMat(worldTransform).multToMat(viewTransform)
            posVTankAimAssist = posVTankAimAssist.multToMat(projectionTransform)
            
            self.miniMap.drawPlayer(self.getLine(), _posV, player.teamId == self.appVars["localPlayerTeamId"])

            if abs(_posVP.w) < 0.001:
                continue
            if _posVP.z > 0:
                continue
            x = self.screenCenterX*(1+_posVP.x/_posVP.w)
            y = self.screenCenterY*(1+_posVP.y/_posVP.w)
            
            xAim = self.screenCenterX*(1+posVTankAimAssist.x/posVTankAimAssist.w)
            yAim = self.screenCenterY*(1+posVTankAimAssist.y/posVTankAimAssist.w)
            
            
            # ---------- draw player distance hint text ---------
            if player.teamId != self.appVars["localPlayerTeamId"]:
                ehfgraphics.drawStringLeft(self.getFont(), 
                                           x+5, 
                                           y+5, 
                                           10, 
                                           40, 
                                           _color, 
                                           "%0.1f" % distant)

            # ---------- draw a spot for tank aim assist -----------
                ehfgraphics.drawSpot(self.getLine(),
                                     xAim,
                                     yAim, 
                                     _color,
                                     size=1.5)
                
                ehfgraphics.drawLine(self.getLine(), x , y, xAim-x, yAim-y, 0.5, color=_color)
                
            # ---------- draw boxed esp -------------
            _width, _height = self.getWidthHeight(distant)
            if player.poseType:
                y = y + _height/2.0
            x = x - _width/2.0
            ehfgraphics.drawBox(self.getLine(), 
                                x, 
                                y, 
                                _width, 
                                _height, 
                                2, 
                                _color)
            
            # --------- draw tank aim hint -------------
            # DEPRECATED!!
#            if almostFEq( self.appVars["fov_y"], 0.349065870047, 4 ):
#                self.drawTankAimHint3x(distant, hintColor, x, y, _height, deltaY)
#            elif almostFEq( self.appVars["fov_y"], 0.872664630413, 4 ):
#                self.drawTankAimHint1x(distant, hintColor, x, y, _height, deltaY)
            

    def drawTankAimHint3x(self, distant=0.0, hintColor=0x0, x=0.0, y=0.0, _height=0.0, deltaY=0.0):
        hintHeight = 0.0
        if distant < 50.0 or distant > 800:
            return
        elif distant >=50.0 and distant < 200:
            hintHeight = y+_height-(distant-50.0)/150.0*53
        elif distant > 200 and distant <= 400:
            hintHeight = y+_height-(distant-200.0)/200.0*20-53
        elif distant > 400 and distant <= 500:
            hintHeight = y+_height-(distant-400.0)/100.0*30-73
        elif distant > 500 and distant <= 600:
            hintHeight = y+_height-(distant-500.0)/100.0*31-103
        elif distant > 600 and distant <= 700:
            hintHeight = y+_height-(distant-600.0)/100.0*34-134
        elif distant > 700 and distant <= 800:
            hintHeight = y+_height-(distant-700.0)/100.0*36-168
        ehfgraphics.drawSpot(self.getLine(),
                             x,
                             hintHeight, 
                             hintColor,
                             size=2)
        ehfgraphics.drawStringLeft(self.getFont(), 
                                   x+5, 
                                   hintHeight+5, 
                                   10, 
                                   40, 
                                   hintColor, 
                                   "%0.1f" % deltaY)


    def drawTankAimHint1x(self, distant=0.0, hintColor=0x0, x=0.0, y=0.0, _height=0.0, deltaY=0.0):
        hintHeight = 0.0
        if distant < 50.0 or distant > 800:
            return
        elif distant >=50.0 and distant <= 400:
            hintHeight = y+_height-(distant-50.0)/350.0*26
            #return
        elif distant > 400 and distant <= 500:
            hintHeight = y+_height-(distant-400.0)/100.0*12-26
        elif distant > 500 and distant <= 600:
            hintHeight = y+_height-(distant-500.0)/100.0*12-38
        elif distant > 600 and distant <= 700:
            hintHeight = y+_height-(distant-600.0)/100.0*13-50
        elif distant > 700 and distant <= 800:
            hintHeight = y+_height-(distant-700.0)/100.0*14-63
        ehfgraphics.drawSpot(self.getLine(),
                             x,
                             hintHeight, 
                             hintColor,
                             size=2)
        ehfgraphics.drawStringLeft(self.getFont(), 
                                   x+5, 
                                   hintHeight+5, 
                                   10, 
                                   40, 
                                   hintColor, 
                                   "%0.1f" % deltaY)
        
    
    def getWidthHeight(self, distant):
        width, height = 18.0, 26.0
        _f = 20.0 / distant
        width = width * _f
        height = height * _f
        if width < 3:
            width = 3.0
        if height < 3:
            height = 3.0
        return width, height
        
    
    def _validatePlayer(self, player):
        if player.address:
            return True
        else:
            return False
    

def almostFEq(val1, val2, precision=1):
    return round(val1, precision) == round(val2, precision)
    