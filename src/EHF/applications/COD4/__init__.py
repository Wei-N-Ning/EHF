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
    import COD4Application
    if appName == "COD4":
        return COD4Application.Cod4Application(debug=debug, dryRun=dryRun)
    elif appName == "COD4Console":
        return COD4Application.Cod4ConsoleApplication(debug=debug, dryRun=dryRun)
    else:
        logger.error("Unrecognized application name, valid choices are: COD4, COD4Console")