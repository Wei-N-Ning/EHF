from PyQt4 import QtCore
import threading

from config import globalconfig

class AppInerface(object):
    
    def __init__(self):
        self.guiPlugins = []
        self.dataPlugins = []
        self.thread = QtCore.QThread(parent=self)
        
    def addPlugin(self, plugin=None):
        self.plugins.add(plugin)
        
    def draw(self):
        for plugin in self.plugins:
            plugin.draw()
    
    def start(self):
        pass
    

