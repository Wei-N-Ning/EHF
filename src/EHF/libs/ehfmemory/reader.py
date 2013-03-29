from EHF.core.win32types import *

from ctypes import windll
kernel32 = windll.kernel32

from struct import unpack

from EHF.libs import ehfmemory


class MemoryReader(ehfmemory.BaseReader):
    """
    The interface of a memory reader class.
    
    The read is able to both read bulk memory (raw dump) and 
    read the finest bit. But for the sake of performance, it is
    highly suggested to bulk-read memory (for player array etc.)
    then parse the exact values
    """
    
    def readInt(self, address):
        """
        helper method to read and return one integer from the given address
        """
        bufInt = c_int()
        self._rpm(address, bufInt, sizeof(bufInt))
        return bufInt.value
    
    def readFloat(self, address):
        """
        to read and return one float from the given address
        """
        bufFloat = c_float()
        self._rpm(address, bufFloat, sizeof(c_float))
        return bufFloat.value