from EHF.core import entity


class TTAppInfo(entity.AppInfo):
    
    def override(self):
        """
        prototype process attribute....
        """
        self.appName = "EHF Prototype application"
        
        self.isDryRun = True
        
        self.bboxLeft = 400
        self.bboxRight = 800
        self.bboxTop = 200
        self.bboxBottom = 500
        self.resolutionX = 400
        self.resolutionY = 300
        self.centerX = 200
        self.centerY = 150
        self.originX = 600
        self.originY = 100


class TTEnvInfo(entity.EnvInfo):
    pass