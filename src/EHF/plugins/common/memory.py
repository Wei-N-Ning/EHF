from EHF.plugins import base

from ctypes import byref
from ctypes import c_int
from ctypes import windll

user32 = windll.user32

class PerFrameMemReaderPlugin(base.BasePerFrameDataPlugin):
    pass


class PreExecutionMemReaderPlugin(base.BasePreExecutionPlugin):
    pass


# -------- Pre-Execution plugin ---------
class MemoryScannerPlugin(base.BasePreExecutionPlugin):
    """
    This plugin will perform a "partial dump" of the process, exporting a large
    trunk of raw data out of the given memory range. The range is defined in the
    app info per-application.
    
    Then it calls a series of address parsers to get the initial offsets. These
    offsets will be used as the "base offsets" for later dynamic mem reading.
    """
    requirements = [ "AppInfo", "EnvInfo", "ProcessHelper" ]
    contributions = []
    
    def initialise(self):
        pass
    
    def _run(self):
        pass
    

# --------per-frame data plugin -----------
class MemoryReaderPlugin(base.BasePerFrameDataPlugin):
    """
    This plugin will read the process memory for every frame.
    It relies on the scanner to locate the static address (or
    the pointer to arrays).
    
    It populates the data structure for downstream plugin to
    fetch data from.
    """
    requirements = [ "AppInfo" ,"EnvInfo", "MemoryReader" ]
    contributions = []
    
    def initialise(self):
        pass
    
    def _run(self):
        pass