import re
import sys


def getPlatformBitcount():
    """
    Extract the bitcount from sys.version string
    
    @return: the platform bitcount, either 32 or 64
             if it fails to extract the information the return value will be -1,
             it is up to the caller to decide how to handle this situation.
    @rtype : int
    """
    result = re.search("( .. )bit", sys.version)
    if result:
        return int(result.groups()[0].strip())
    return -1
