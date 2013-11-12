import ConfigParser
import sys

from EHF.plugins import base

import logging
logger = logging.getLogger(__name__)


class BF4AppInfoSerializationPlugin(base.BasePreExecutionPlugin):

    requirements = ["AppInfo"]
    contributions = []
    
    DUMP_FILE_PATH = "D:\\temp\\bf4_appinfo_dump.cfg"
    
    def initialise(self):
        self.parser = ConfigParser.ConfigParser()
    
    def _run(self):
        """
        @note: the configure entry name must follow the new convention
        """
        appInfo = self._appAttr["AppInfo"]
        
        data = {}
        primaryVariables = appInfo.primaryVars.copy()
        
        # app
        data["applicationName"] = (appInfo.targetAppName, "str")
        data["pid"] = (self._appAttr["ProcessHelper"].pid, "int")
        data["hProcess"] = (self._appAttr["ProcessHelper"].hProcess, "int")
        
        # window
        data["windowLeft"] = (appInfo.bboxLeft, "int")
        data["windowRight"] = (appInfo.bboxRight, "int")
        data["windowTop"] = (appInfo.bboxTop, "int")
        data["windowBottom"] = (appInfo.bboxBottom, "int")
        data["windowResolutionX"] = (appInfo.resolutionX, "int")
        data["windowResolutionY"] = (appInfo.resolutionY, "int")
        data["windowCenterX"] = (appInfo.centerX, "int")
        data["windowCenterY"] = (appInfo.centerY, "int")
        data["windowOriginX"] = (appInfo.originX, "int")
        data["windowOriginY"] = (appInfo.originY, "int")
        data["windowClass"] = (appInfo.targetAppWindowClass, "str")
        
        for name, contents in data.iteritems():
            self.parser.add_section(name)
            varValue, varType = contents
            self.parser.set(name, "value", varValue)
            self.parser.set(name, "type", varType)
        
        for key, value in primaryVariables.iteritems():
            self.parser.add_section(key)
            self.parser.set(key, "value", "0x%X"%value)
            self.parser.set(key, "type", "hexstr")
            
        with open(self.DUMP_FILE_PATH, 'w') as fp:
            self.parser.write(fp)
        logger.info("+ Saved data to %s" % self.DUMP_FILE_PATH)
        
        sys.exit(0)