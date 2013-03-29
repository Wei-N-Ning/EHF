from EHF.libs import ehfmemory
from EHF.libs import ehfmodule

from ctypes import create_string_buffer, c_int, sizeof


class MemoryScannerError(Exception):
    pass


class MemoryScanner(ehfmemory.BaseReader):
    """
    The interface of a memory scanner class.
    
    The scanner will first get a large trunk of raw dump from the given
    memory range, then use the pre-defined pattern-finder to search for
    the addresses.
    
    The pattern-finders are sort of mini-plugin objects that are defined per
    application; without patternfinders the scanner merely dumps a large trunk
    of memory and returns
    
    * One application should own only one instance of this Scanner class
    and should only call once of the scanning function.    
    """
    
    def __init__(self, hProcess, 
                       memoryStart=0x0, 
                       memorySize=0x0,
                       patternFinderRepoClass=""):
        self.hProcess = hProcess
        self.rawDump = create_string_buffer(memorySize)
        self.memoryStart = memoryStart
        self.memorySize = memorySize
        self.values = {}
        
        # get the pattern finder repository class
        className = patternFinderRepoClass.split('.')[-1]
        modulePath = '.'.join( patternFinderRepoClass.split('.')[:-1] )
        repoCls = ehfmodule.getClass(modulePath, className)
        if not repoCls:
            raise MemoryScannerError, "Can not resolve pattern finder repo class:\n%s" % patternFinderRepoClass
        self.patternFinders = repoCls().getRepo()
        
    def run(self):
        # perform the raw dump
        self._rpm(address=self.memoryStart, 
                  buf=self.rawDump, 
                  length=self.memorySize)
        # iterate over the list of pattern finder objects
        for pf in self.patternFinders:
            pf.registerScanner(self)
            pf.run()
            
            self.values[pf.label] = pf.values[0]
            
            # [IMPORTANT]: the "addressExtension" mechanism on the patternfinder has been refactored into a new class:
            # PatternFinderFollower
            
    def valuesToString(self):
        """
        return a print-friendly string of the label-value mapping
        """
        result = "\n ----------- memory scanner ----------- \n"
        for k,v in self.values.items():
            result += "  %s : 0x%X\n" % (k, v)
        result +=  ' -------------------------------------- \n'
        return result