class BaseNode(object):
    def __init__(self, name, **kwargs):
        self.connection = None
        self.data = None
        self.name = name
        self.parameters = kwargs.copy()
        self.initialise()
        
    def connectToUpstream(self, node):
        self.connection = node
        
    def updateFromUpstream(self):
        self.data = self.connection.getData()
        
    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data
    
    def initialise(self):
        pass
    
    def _cook(self):
        pass
    
    def cook(self):
        if self.connection:
            self.connection.cook()
            self.updateFromUpstream()
            self._cook()
        else:
            self._cook()
            
#if __name__ == "__main__":
#    BaseNode("asd")