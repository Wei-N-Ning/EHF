"""
here defines the base interface of the pattern finder class
"""
import re
import ctypes
from EHF.core import win32types
from binascii import unhexlify



class PatternFinderError(Exception):
    pass


class StaticFinder(object):
    """
    
    To define a static address.
    In reality, this should NEVER be used, as every time the game gets
    patched all the static addresses will change.
    
    It basically just adds the label:address pair, and if it's a pointer,
    it will perform de-pointer
    
    """
    def __init__(self, label="", niceName="", address=0x0, isPointer=False):
        self.label = label
        self.niceName = niceName if niceName else label
        self.address = address
        self.values = []
        self.isPointer = isPointer
        
    def registerScanner(self, memoryScanner):
        self.scanner = memoryScanner
    
    def run(self):
        value = self.address
        if self.isPointer:
            _value = win32types.c_int32
            self.scanner._rpm(self.address, _value, win32types.sizeof(win32types.c_int32))
            value = _value.value
        self.values.append(value)
        
        
        
class PatternFinder(object):
    """
    
    To find the address by the given pattern.
    
    """
    def __init__(
                 self, 
                 label="",
                 niceName="",
                 patternExpected="", 
                 patternMask="",
                 patternMatch="FF",
                 valueOffsets=[], 
                 addressExpected=0x0,
                 allowMultiFinds=False,
                ):
        """
        @param label: used for internal indexing (particularly for appInfo.primaryVars)
        @type  label: str
        
        @param niceName: print-friendly name, optional
        @type  niceName: str
        
        @param patternExpected: the target hex pattern, copied from IDA pro
        @type  patternExpected: str
        
        @param patternMask: a string consists of only FF or 00, this is a commonly used technique
        @type  patternMask: str
        
        @param patternMatch: works together with patternMask
        @type  patternMatch: str
        
        @param valueOffsets: a list of (offset, type, type_length) tuples.
                             finder will perform additional RPM() to get the 
                             exact value
        @type  valueOffsets: list
        
        @param addressExpected: the expected address, currently not used....
        @type  addressExpected: int
        
        @param allowMultiFinds: normally should be False, haven't met a case where we
                                need to enable this flag
        @type  allowMultiFinds: bool
        
        [IMPORTANT] how to count offset:
        say the * part is the starting address of the actual data we look for...
                patternExpected="8B 06 8B 50 20 8B CE FF D2 8B 0D 24 3C AA 02 8B 86 9C 03 00 00 89 41 28",
                patternMask    ="FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF FF",
                               # 1  2  3  4  5  6  7  8  9  A  B  *, that why the offset is 0xB!
        
        """
        self.label = label
        self.niceName = niceName if niceName else label
        
        self.patternExpected = unhexlify( patternExpected.replace(' ', '') )
        self.patternMask = unhexlify( patternMask.replace(' ', '') )
        self.patternMatch = unhexlify( patternMatch ) 
        
        self.patternFound = []
        
        # value offsets: [(offset, datatype), (offset, datatype)... ...  ]
        self.valueOffsets = valueOffsets
        self.values = []
        self.addressExpected = addressExpected
        
        self.scanner = None
        
        self.allowMultiFinds = allowMultiFinds
        
    def registerScanner(self, memoryScanner):
        self.scanner = memoryScanner
    
    def run(self):
        self._find()
        self._unpackValues()
    
    def _find(self):
        """
        find all the locations from the scanner raw dump that 
        match with the search pattern
        """
        if not self.scanner.rawDump:
            raise PatternFinderError,\
                  "Scanner dump is invalid!"
        pattern = ''
        for i in range(len(self.patternExpected)):
            if self.patternMask[i] == self.patternMatch:
                pattern += re.escape( self.patternExpected[i] )
            else:
                pattern += '.'
        result = list(
                      re.finditer( pattern, self.scanner.rawDump, re.DOTALL )
                      )
        if len(result) == 0:
            raise PatternFinderError,\
                  "Can not find pattern for [%s]!" % self.label
        elif len(result) > 1 and not self.allowMultiFinds:
            raise PatternFinderError,\
                  "Found %d results for [%s], not accepted!" % (len(result), self.label)
        self.patternFound = [self.scanner.memoryStart + f.start() for f in result]
        return True
    
    def _unpackValues(self):
        """
        trace and unpack the values from the found locations
        
        * Note: I will get into trouble if later on the "allowMultiFinds" flag
        is turned on, but that should be a very rare case...
        
        * Also note that it calls rpm() again just for those short entries...
        it'd great if I just parse the raw dump... leave it for now
        """
        for eachFound in self.patternFound:
            for entry in self.valueOffsets:
                offset, datatype, datasize = entry
                data = datatype()
                self.scanner._rpm(eachFound+offset, data, datasize)
                self.values.append(data.value)
    


class PatternFinderFollower(object):
    """
    
    To find the address by displacing the previously acquired addresses.
    i.e. to do $address+offset or *($address+offset) 
    
    """
    def __init__(self,
                 label="",
                 niceName="",
                 baseVariableName="",
                 isPointer=False,
                 valueOffsets=[]):
        """
        see PatternFinder class for argument types.
        
        Note: 
        baseVariableName is the label/name of one of the previous pattern finder,
        with the its address at hand, the follower is able to add the offset and/or
        get the pointer value
        
        the isPointer flag is to tell the scanner(memReader) whether it should
        evaluate the value of the address (which in C is called de-pointer)
        """
        self.label = label
        self.niceName = niceName if niceName else label
        self.baseVariableName = baseVariableName
        self.isPointer = isPointer
        self.valueOffsets = valueOffsets
        self.values = []
        
    def registerScanner(self, memoryScanner):
        self.scanner = memoryScanner

    def run(self):
        baseVar = self.scanner.values[self.baseVariableName]
        newVar = baseVar+self.valueOffsets[0]
        if self.isPointer:
            _value = win32types.DWORD()
            self.scanner._rpm(newVar, _value, ctypes.sizeof(win32types.DWORD))
            newVar = _value.value
        self.values = [ newVar, ]