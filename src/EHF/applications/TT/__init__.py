"""
a test application for the graphic stuffs
"""

import logging
logger = logging.getLogger(__name__)

def getPreset(presetClassName=""):
    """
    return an instance of the the preset config
    """
    presetModule = __import__(name="presets")
    presetClass = getattr(presetModule, presetClassName, None)
    if presetClass:
        return presetClass()
    else:
        raise KeyError, "Can not find [%s] preset from ./presets.py" % presetClassName
    
def getApp(appName, debug, dryRun):
    """
    return an instance of the application
    """
    import TTApplication
    if appName == "TT":
        return TTApplication.TTApplication(debug=debug, dryRun=dryRun)
    elif appName == "TTConsole":
        return TTApplication.TTConsoleApplication(debug=debug, dryRun=dryRun)
    else:
        logger.error("Unrecognized application name, valid choices are: TT, TTConsole")