"""
to launch an EHF application, type:
python launch.py -h/--help for complete description
"""


import sys
import optparse

import logging
logger = logging.getLogger(__name__)
logging.basicConfig()

logging.root.setLevel(logging.INFO)


def main():
    options, _ = getOptionsAndArgs()
    appName   = options.application
    appPreset = options.presetName
    isDebug   = options.debug
    isDryRun  = options.dryRunMode
    try:
        appModule = __import__("EHF.applications.%s"%appName.replace("Console", ''), fromlist=["applications", appName])
    except ImportError:
        logger.error("Can not load application [%s]" % appName)
        sys.exit(1)
    logger.info("Loaded application [%s], preset [%s], debug: %s, dry-run: %s" % (appName, appPreset, isDebug, isDryRun))
    logger.info(appModule.__name__)
    appInstance = appModule.getApp(appName=appName, debug=isDebug, dryRun=isDryRun)
    
    try:
        appInstance.execute()
    except KeyboardInterrupt:
        logger.info("User stopped execution!")
        appInstance.terminate()
        appInstance.release()
        sys.exit(0)
    except Exception, e:
        logger.error("An error occurred during execution! Reason: %s" % e)
        sys.exit(1)


def getOptionsAndArgs():
    """
    @return: option instance, argument list;
             only the former is useful
    @rtype : (option, list)
    """
    usage =\
"""
python launch.py [options]

for example, to launch EHF-COD4:
python launch.py --app=COD4

to launch EHF-COD7 with debug flag on:
python launch.py --app=COD7 --debug
"""
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--app", 
                      dest="application",
                      help="the name of the application which will be used to import the application module, e.g. COD4, BF3......")
    parser.add_option("--preset",
                      dest="presetName",
                      default="Standard",
                      help="the name of the application preset, which contains a series of configuration")
    parser.add_option("-d",
                      "--debug",
                      action="store_true",
                      dest="debug",
                      default=False,
                      help="to active the debug mode for the given application, note that not every application has this mode")
    parser.add_option("-n",
                      "--dry-run",
                      action="store_true",
                      dest="dryRunMode",
                      default=False,
                      help="start the application in dry-run mode, meaning use pre-generated mock data rather than live data")
    return parser.parse_args()


if __name__ == "__main__":
    main()