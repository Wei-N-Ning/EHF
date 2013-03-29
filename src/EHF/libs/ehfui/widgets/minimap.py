import copy

from EHF.libs import ehfgraphics
from EHF.libs.ehfmaths import types as ehfmaths_types



class BaseMiniMap(object):
    """
    The base interface of the minimap widget.
    
    It is a rectangle area display player positions and (optionally) moving directions.
    Depends on the subclass settings, it could be view-oriented, meaning the axis of the
    minimap will always be aligned with the viewing camera, which requires all the players'
    position vector to be transformed into the view space;
    It could also be view-independent, meaning it just literally draw all the players (
    including the view origin) with their world transform, it could be useful when having
    the actual bitmap of the map (COD series), thus it's identical to the in-game air supply
    minimap...
    
    Sub-classes are to implement the drawing method as well as the bitmap display method...            
    """
    def __init__(self, 
                 # location control
                 centerX=0, centerY=0, boundaryX=0, boundaryY=0,
                 # color/drawing style
                 borderWidth=3, lineWidth=3, selfColor=0xFF00FF00, teamColor=0xFF1111FF, enemyColor=0xFFFF1111, boundaryColor=0xFF1111FF,
                 # size/scale control
                 scale=2, spotSize=3,
                 # other attributes
                 **kwargs
                 ):
        """
        TODO: change the absolute centerX, centerY to use the relative calculation corresponding the window rect,
              thus it works for the floating window mode as well
        
        @param centerX, centerY: the relative center coords of the minimap in regards to
                                 the display window
                                 for example, if centerX, centerY = 10, 10, then the drawing will start from the window's edge plus 10 pixel 
                                 downward and rightward, 
                                 IT IS A RELATIVE VALUE!
                                 to calculate the center: boundary + border_width
        @type  centerX, centerY: int
        
        @param boundaryX, boundaryY: the size limit of this minimap
        @type  boundaryX, boundaryY: int
        """
        self.centerX = centerX
        self.centerY = centerY
        self.boundaryX = boundaryX
        self.boundaryY = boundaryY
        
        self.borderWidth = borderWidth
        self.lineWidth = lineWidth
        
        self.selfColor = selfColor
        self.teamColor = teamColor
        self.enemyColor = enemyColor
        self.boundaryColor = boundaryColor
        
        self.scale = scale
        self.spotSize = spotSize
        
        self._initAttributes(kwargs)
        
    def _initAttributes(self, argDict):
        """
        to initialize the attributes required by the sub-classes
        """
        pass
    
    def setScale(self, scaleFactor):
        self.scale = scaleFactor
        
    def drawSelf(self, line):
        ehfgraphics.drawSpot55WithDot(line,
                                      self.centerX, 
                                      self.centerY, 
                                      self.selfColor)
        
    def drawPlayer(self, line, playerPosition, sameTeam=False):
        pass
    
    def drawBoundary(self, line):
        ehfgraphics.drawBox(line, 
                            self.centerX-self.boundaryX, 
                            self.centerY-self.boundaryY, 
                            self.boundaryX*2, 
                            self.boundaryY*2, 
                            self.borderWidth, 
                            self.boundaryColor)
    


class SimpleMiniMap(BaseMiniMap):
    """
    This widget draws a mini-map
    
    It requires at least one of these source data (passed in via the **kwargs)

    1. (COD style) view axis, view origin and player positions, player yaw/pitch
       * viewAxisZ
    
    2. (frostbite style) viewForward vector, player position-vectors in camera(view)-space, player view vectors
       * vecForward
    """
    def _initAttributes(self, argDict):
        # to transform object from world space to camera space
        self.vecForward = argDict.get("vecForward", None)
        # required to compensate for the pitch of the camera
        self.viewAxisZ = argDict.get("viewAxisZ", None)
        
    def setVecForward(self, vecForward):
        self.vecForward = vecForward
    
    def setViewAxisZ(self, viewAxisZ):
        self.viewAxisZ = viewAxisZ
    
    def _getYCoord(self, position):
        """
        Use this method to compensate for the incorrect scale caused by pitch, the theory is:
        
        1. since position is a pos-vector in the view-space, the y-z derivative of this pos-vector
           and the viewForward vector form the y-z plane
        2. by trig definition:
           y = pos.z / pos.w / cos(A)
           * A is angle between the the y-z plane derivative of the camera forward vector
             and the position vector, all normalized 
        
        This will ensure pitching the view camera will not change the projected x, z coords (i.e. x, y coords in the minimap)
        """
        cosA = self.vecForward.dotProduct( ehfmaths_types.VECTOR4( self.vecForward.x, 0.0, self.vecForward.z, 0.0).normalize() )
        return position.z / position.w / abs(cosA) * self.scale
        
    def drawPlayer(self, line, position, tm=True):
        _color = self.teamColor if tm else self.enemyColor
        # it's not necessary, the view transformation won't modify the w element
        if not position.w > 0.001:
            return
        _x = position.x / position.w * self.scale
        _y = self._getYCoord(position)#position.z / position.w * self.scale
        _x += self.centerX
        _y += self.centerY
        
        if _x > (self.centerX+self.boundaryX):
            _x = self.centerX+self.boundaryX
        elif _x < (self.centerX-self.boundaryX):
            _x = self.centerX-self.boundaryX
        if _y > (self.centerY+self.boundaryY):
            _y = self.centerY+self.boundaryY
        elif _y < (self.centerY-self.boundaryY):
            _y = self.centerY-self.boundaryY
        
        ehfgraphics.drawSpot55WithDot(line, _x, _y, _color)