import sys

from EHF.plugins import base

import logging
logger = logging.getLogger(__name__)


class SimpleInteracterPlugin(base.BasePerFrameDataPlugin):
    
    """
    This plugin provides a simple interpreter-like command line interface that
    waits for the user to type in command (could be python commands) and passes
    the command string to the executor
    
    For example, the user can type in "print dir(app)" or other immediate command, 
    and also can evoke a function or script by type in the name of the function...,
    the user can skip the interacter and wait for all the current per-frame
    plugins finish execution, then the interacter will appear again and wait for
    further instruction 
    
    * IMPORTANT: this plugin is only supposed to be used in a console application,
    attempt to run this plugin in a graphic application will produce unexpected result!!
    """
    
    requirements = [ "AppInfo", "EnvInfo" ]   
    contributions = []
    
    def initialise(self):
        self.cmdString = ""
        
        # for the convenience...
        self.parser = CmdParser(self._appAttr["AppInfo"], self._application)
        
    def _run(self):
        while self.getUserInput() != '\n':
            self.parseUserInput()
    
    def getUserInput(self):
        sys.stdout.write("[EHF cmd] ")
        self.cmdString = sys.stdin.readline()[:-1] #get rid of the trailing new line character
        return self.cmdString
    
    def parseUserInput(self):
        self.parser.parse(self.cmdString)
    

class CmdParser(object):
    """
    A command string parser, responsible to evaluate the user input
    and (if needed) call the corresponding functions.
    """
    def __init__(self, appInfo, application):
        self.appInfo = appInfo
        self.application = application
        
    def parse(self, cmdString):
        try:
            exec(cmdString)
        except Exception, e:
            logger.error("Failed to execute user command. Reason: %s" % e)