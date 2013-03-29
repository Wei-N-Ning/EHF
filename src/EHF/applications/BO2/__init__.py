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
    import BO2Application
    if appName == "BO2":
        return BO2Application.BO2Application(debug=debug, dryRun=dryRun)
    elif appName == "BO2Console":
        return BO2Application.BO2ConsoleApplication(debug=debug, dryRun=dryRun)
    else:
        logger.error("Unrecognized application name, valid choices are: BO2, BO2Console")