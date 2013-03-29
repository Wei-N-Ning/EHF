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
    import BF3Application
    if appName == "BF3":
        return BF3Application.BF3Application(debug=debug, dryRun=dryRun)
    elif appName == "BF3Console":
        return BF3Application.BF3ConsoleApplication(debug=debug, dryRun=dryRun)
    else:
        logger.error("Unrecognized application name, valid choices are: BF3, BF3Console")
