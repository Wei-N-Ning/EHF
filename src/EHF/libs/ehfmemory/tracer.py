"""
here defines the base interface of the address-tracer class
"""

from EHF.core.win32types import *

from ctypes import windll
kernel32 = windll.kernel32

from struct import unpack

from EHF.libs import ehfmemory

class TracerError(Exception):
    pass


class MemoryTracer(ehfmemory.BaseReader):
    """
    The interface of a memory tracer.
    
    The tracer is able to automatically trace the references from object/ptr to
    object/ptr. 
    """
    pass