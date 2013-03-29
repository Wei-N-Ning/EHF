from EHF.libs import ehfgraphics
from EHF.plugins import base

import logging
logger = logging.getLogger(__name__)


# ------- static drawing plugin  -------
class SimpleCrosshairPlugin(base.BasePerFrameDrawingPlugin):
    """
    static drawing.
    draw a crosshair
    """
    requirements = [ "WindowFrame", "AppInfo", "EnvInfo" ]
    contributions = []
    
    def initialise(self):
        self.cX = self._appAttr["AppInfo"].resolutionX / 2
        self.cY = self._appAttr["AppInfo"].resolutionY / 2
        self.size = self._appAttr["EnvInfo"].crossHairSize
        self.width = self._appAttr["EnvInfo"].crossHairLineWidth
        self.color = self._appAttr["EnvInfo"].crossHairLineColor
        self.style = self._appAttr["EnvInfo"].crossHairStyle
        
        # IMPORTANT: need to "trap" execution here somehow....
        logger.info( "cX: %d, cY: %d, size: %d, width: %d, color: %d, style: %d" %\
                     (self.cX,self.cY,self.size,self.width,self.color,self.style) )
        
    def _run(self):
        if self.style == 1:
            ehfgraphics.drawXCrosshair(self.getLine(), self.cX, self.cY, self.size, self.width, self.color)
        else:
            ehfgraphics.drawCrosshair(self.getLine(), self.cX, self.cY, self.size, self.width, self.color)


class SimpleBoxPlugin(base.BasePerFrameDrawingPlugin):
    """
    static drawing.
    test drawing a simple box
    """
    requirements = [ "WindowFrame", "AppInfo", "EnvInfo" ]
    
    def initialise(self):
        self.oX = self._appAttr["AppInfo"].resolutionX / 2
        self.oY = self._appAttr["AppInfo"].resolutionY / 2
        
        #logger.info( "oX: %d, oY: %d" %  (self.oX, self.oY) )
        
    def _run(self):
        ehfgraphics.drawBox(self.getLine(), self.oX, self.oY, 50, 50, self.getclw(), self.getclc())
        

class SimpleTextPlugin(base.BasePerFrameDrawingPlugin):
    """
    draw texts
    
    divide the canvas into 4 region (up, down, right, left), 
    the region ids are (0, 1, 2, 3)
    
    the display text list consists of (region, text) tuples
    """
    requirements = [ "WindowFrame", "AppInfo", "EnvInfo" ]
    
    regionMapping = {0: (-2, -2), 1: (1, -2), 2: (-1, 1), 3: (-2, -1)}
    
    def initialise(self):
        self.fontColor = self._appAttr["EnvInfo"].fontColor
        self.fontWidth = self._appAttr["EnvInfo"].fontWidth
        self.fontHeight = self._appAttr["EnvInfo"].fontHeight
        self.fontMargin = self._appAttr["EnvInfo"].fontMargin
        self.rx = self._appAttr["AppInfo"].resolutionX
        self.ry = self._appAttr["AppInfo"].resolutionY
        self.ux = self.rx / 4
        self.uy = self.ry / 4
        self.cx = self.rx / 2
        self.cy = self.ry / 2
        
        #logger.info( "SimpleTextPlugin initialised" )
        
    def getPosByRegionId(self, regionId=0, index=0):
        """
        return (x, y) for the drawText function
        """
        ridx, ridy = self.regionMapping[regionId]
        px = self.cx + self.ux * ridx
        py = self.cy + self.uy * ridy
        return (3+px, 3+py+(self.fontHeight+self.fontMargin)*index)
    
    def _run(self):
        regionIndexes = {0:0, 1:0, 2:0, 3:0}
        if len(self._appAttr["AppInfo"].displayTextList):
            for regionId, text in self._appAttr["AppInfo"].displayTextList:
                _x, _y = self.getPosByRegionId(regionId, regionIndexes[regionId])
                ehfgraphics.drawStringLeft(self.getFont(), 
                                           _x, _y,
                                           self.fontWidth, 
                                           self.fontHeight, 
                                           self.fontColor, 
                                           text)
                regionIndexes[regionId] += 1
        if len(self._appAttr["AppInfo"].titleTextList):
            for regionId, text in self._appAttr["AppInfo"].titleTextList:
                _x, _y = self.getPosByRegionId(regionId, regionIndexes[regionId])
                ehfgraphics.drawStringLeft(self.getFont(), 
                                           _x, _y,
                                           self.fontWidth, 
                                           self.fontHeight, 
                                           self.fontColor, 
                                           text)
                regionIndexes[regionId] += 1
                
                
# ------- dynamic drawing plugin  -------
