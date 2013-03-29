from ctypes import byref

from ctypes import windll

from ctypes import POINTER
kernel32 = windll.kernel32

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)



class ReadProcessMemoryError(Exception):
    pass


class BaseReader(object):
    """
    The base interface of the memory reader and scanner.
    
    These two spin-offs define two different approaches of RPM:
    reader try its best to convert the raw data to some meaningful
    data structures,
    whereas scanner try its best to find pattern from the raw data and mark
    the addresses where such pattern appears;
    
    Reader is supposed to be called in a dynamic running context (ie.
    the main loop of the application) without a noticable overhead;
    Whereas scanner should only run once during the entire execution 
    cycle as it may take considerable amount of time to retrieve and
    parse the raw data
    
    Both of them can only work with a given process handle. Typically
    this process handle is possessed by the process helper.
    """
    
    def __init__(self, hProcess):
        self.hProcess = hProcess
        
    def _rpm(self, address, buf, length):
        """
        a convenient wrapper of kernel32 RPM
        @param address: starting address
        @param buf: string buffer object, ctypes.create_string_buffer()
        """
        if not kernel32.ReadProcessMemory(self.hProcess, address, byref(buf), length, None):
            raise ReadProcessMemoryError, "Can not read memory from process [%d], address [%x], length [%d]" % (self.hProcess, address, length)
        else:
            logger.debug(" + Dumpped memory from process [%d], address [%x], length[%d]" % (self.hProcess, address, length))