"""
The bf4 application package
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
    import BF4Application
    if appName == "BF4":
        return BF4Application.BF4Application(debug=debug, dryRun=dryRun)
    elif appName == "BF4Console":
        return BF4Application.BF4ConsoleApplication(debug=debug, dryRun=dryRun)
    else:
        logger.error("Unrecognized application name, valid choices are: BF4, BF4Console")
        return None