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
        data["applicationName"] = appInfo.targetAppName
        
        # window
        data["windowLeft"] = appInfo.bboxLeft
        data["windowRight"] = appInfo.bboxRight
        data["windowTop"] = appInfo.bboxTop
        data["windowBottom"] = appInfo.bboxBottom
        data["windowResolutionX"] = appInfo.resolutionX
        data["windowResolutionY"] = appInfo.resolutionY
        data["windowCenterX"] = appInfo.centerX
        data["windowCenterY"] = appInfo.centerY
        data["windowOriginX"] = appInfo.originX
        data["windowOriginY"] = appInfo.originY
        data["windowClass"] = appInfo.targetAppWindowClass
        
        self.parser.add_section("data")
        for key, value in data.iteritems():
            self.parser.set("data", key, value)
        self.parser.add_section("primary")
        for key, value in primaryVariables.iteritems():
            self.parser.set("primary", key, value)
        with open(self.DUMP_FILE_PATH, 'w') as fp:
            self.parser.write(fp)
        logger.info("+ Saved data to %s" % self.DUMP_FILE_PATH)
        
        sys.exit(0)