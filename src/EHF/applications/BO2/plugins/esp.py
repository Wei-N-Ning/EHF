"""
esp is a complex system because it requires all type of data, player, entity, viewOrigin....
producing esp is however a simple process: iterate over players/entities; get their rect and pos; draw

esp is configured by each application, such as the rect size, ratio and whether to draw the player/entity name 
and distance; whether to draw the vis-line etc etc....

the simplest esp consists of the rect and the name.... and if possible, the health bar
"""

from EHF.libs import ehfgraphics
from EHF.plugins import base
from EHF.applications.BO2 import datastruct
from EHF.libs import ehfmaths
from EHF.libs.ehfmaths import types as ehfmaths_types
from EHF.libs.ehfui import widgets


class EspPlugin(base.BasePerFrameDrawingPlugin):
    """
    Draw the esp
    """
    def initialise(self):
        self.colorTeammate = self._appAttr["EnvInfo"].boxLineColorAlt
        self.colorEnemy    = self._appAttr["EnvInfo"].boxLineColor
        self.lineWidth = self._appAttr["EnvInfo"].boxLineWidth
        self.appVars = None
        self.appInfo = None
        
        self.miniMap = None
        
        self.hasInitialized = False
    
    def delayedInit(self):
        if not self.hasInitialized:
            self.appVars = self._appAttr["AppInfo"].vars
            self.appInfo = self._appAttr["AppInfo"]
            self.hasInitialized = True
            self.miniMap = widgets.SimpleMiniMap(vecForward=None, 
                                                 centerCoord=ehfmaths_types.COORD(150, 300),
                                                 boundaryX=140, boundaryY=140, 
                                                 lineWidth=3, 
                                                 tmColor=0xFF1111FF, enColor=0xFFFF1111, boundaryColor=0xFFFF1111, 
                                                 scale=2,
                                                 viewAxisZ=None)
            
    def _run(self):
        # delayed init
        self.delayedInit()
        for player in self.appVars["players"][1:]:
            # mini map
            self.miniMap.drawBoundary(self.getLine())
            self.miniMap.drawSelf(self.getLine())
            delta = (player.pos - self.appVars["viewOrigin"]).toPyVector4P()
            self.miniMap.drawPlayer(self.getLine(), delta, tm=True)
        
    
    def _validatePlayer(self, player):
        """
        example (@externalHack)
        if (p.type == ET_PLAYER) and p.valid and p.alive and p != read_game.my_player:
        """
        if player.type == datastruct.ET_PLAYER and player.alive:
            return True
        else:
            return False
        
    
    def _drawPlayerEsp(self, player):
        """
        example:
        self.getLine()
        
        drawBox(line, x, y, w, h, width, color):
            w, h: width and height of the box,
            x, y: top-left corner
        """
        _color = self.colorTeammate if player.team == self.appVars["myTeam"] \
                                    else self.colorEnemy
        feet, head, sizeX, sizeY = self._calculatePlayerScreenSize(player)
        if feet and head:
            ehfgraphics.drawBox(self.getLine(), feet.x - sizeX/2, feet.y, sizeX, -sizeY, self.lineWidth, _color)
    
    def _calculatePlayerScreenSize(self, player, height=60):
        centerX = self.appVars["refdef_width"]/2
        centerY = self.appVars["refdef_height"]/2
        # not the real pos!!
        _headPos = ehfmaths.VECTOR(player.pos.x, player.pos.y, player.pos.z+height)
        feet = ehfmaths.worldToScreen(self.appVars["fov_x"], 
                                      self.appVars["fov_y"], 
                                      centerX, 
                                      centerY, 
                                      self.appVars["viewAxis"][0], 
                                      self.appVars["viewAxis"][1], 
                                      self.appVars["viewAxis"][2], 
                                      self.appVars["viewOrigin"], 
                                      player.pos)
        head = ehfmaths.worldToScreen(self.appVars["fov_x"], 
                                      self.appVars["fov_y"], 
                                      centerX, 
                                      centerY, 
                                      self.appVars["viewAxis"][0], 
                                      self.appVars["viewAxis"][1], 
                                      self.appVars["viewAxis"][2], 
                                      self.appVars["viewOrigin"], 
                                      _headPos)
        sizeX, sizeY = 0, 0
        if feet and head:
            sizeY = feet.y - head.y
            sizeX = sizeY / 2.75          # standing up
            if sizeY < 10:     
                sizeY = 10
        return (feet, head, sizeX, sizeY)
        
