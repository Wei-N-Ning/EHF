"""
to parse c struct declaration and generate the corresponding python class (structure)
"""
from pprint import pprint as pp


typeMapping = {
               "char" : ("c_char", 1),
               "int"  : ("c_int", 4),
               "float": ("c_float", 4),
               "__int64": ("c_int64", 8),
               "byte": ("c_byte", 1),
               "BYTE": ("c_byte", 1),
               "DWORD":("c_int", 4),
               "bool":("c_int", 4),
               }

unsignedTypeMapping = {
                       "int" : ("c_uint", 4),
                       "__int16" : ("c_uint16", 2),
                       "__int32" : ("c_uint32", 4),
                       "__int64" : ("c_uint64", 8),
                       "byte"    : ("c_ubyte", 1),
                       }


class CVarParser(object):
    def __init__(self, rawLine=""):
        self.rawLine = rawLine
        self.typeName = ""
        self.type = None
        self.typeLength = 0
        self.name = ""
        self.isArray = False
        self.elementCount = 1
        self.initValue = None
        self.isUnsigned = False
        self.isTyped = False
        self.isSolved = False
        self._parseLine(rawLine)
        
    def _parseLine(self, rawLine=""):
        for segment in rawLine.split(' '):
            if not segment:
                continue
            elif segment == "unsigned":
                self.isUnsigned = True
            elif self.isTyped:
                if '[' in segment:
                    self.isArray = True
                    self.name = segment.split('[')[0]
                    self.elementCount = int( segment.split('[')[-1].split(']')[0] )
                else:
                    self.name = segment
            else:
                self.typeName = segment
                if self.isUnsigned:
                    self.type, self.typeLength = unsignedTypeMapping.get(segment, (None, 0))
                
                else:
                    self.type, self.typeLength = typeMapping.get(segment, (None, 0))
                self.isTyped = True
        if self.type and self.typeLength:
            self.isSolved = True
    
    def getSize(self):
        return self.typeLength*self.elementCount if self.isArray else self.typeLength
    
    def __repr__(self):
        result = "%s %s"%(self.type, self.name)
        if self.isArray:
            result += "[%d]"%self.elementCount
        result += " 0x%X"%(self.typeLength * self.elementCount)
        return result
    
    def __str__(self):
        return self.__repr__()
    

class CStructParser(object):
    def __init__(self, rawContents=[]):
        self.rawLines = []
        self.isClosed = False
        self.vars = [] # list of CVarParsers
        self.name = ""
        self._parseBlock(rawContents)
    
    def getStructSize(self):
        return sum( [ _var.getSize() for _var in self.vars ] )
    
    def isSolved(self):
        return all(  [ eachVar.isSolved for eachVar in self.vars ]  )
        
    def _parseBlock(self, rawContents=[]):
        for eachLine in rawContents:
            eachLine = eachLine.replace('\n', '').replace(';', '')
            if not eachLine or eachLine.startswith('{'):
                continue
            elif eachLine.startswith("struct"):
                self.name = eachLine.replace(' ', '').split("struct")[-1]
            elif eachLine.startswith('}'):
                self.isClosed = True
            else:
                self.rawLines.append(eachLine)
                self.vars.append( CVarParser(eachLine) )
    
    def __repr__(self):
        return "-------- struct %s --------\n%s\n-------------------" % (self.name, '\n'.join( str(eachVar) for eachVar in self.vars ))
    
    def __str__(self):
        return self.__repr__()
    
class Parser(object):
    def __init__(self, rawContents=[]):
        """
        rawContents are the raw lines from readlines() 
        """
        self.structs = []
        self._parseBlocks(rawContents)
        
    def _parseBlocks(self, rawContents=[]):
        """
        to detect struct block boundary
        """
        markStart = markEnd = idx = 0
        for eachLine in rawContents:
            if eachLine.startswith('struct'):
                markStart = idx
            elif eachLine.startswith('}'):
                markEnd = idx
            idx += 1
            if markEnd > markStart:
                self.structs.append( CStructParser(rawContents[markStart:markEnd+1]) )
            
            
            
if __name__ == "__main__":
    fh = open("tests/testheaderone.h")
    #cStructP = CStructParser(fh.readlines())
    #print "0x%X"%cStructP.getStructSize()
    par = Parser(fh.readlines())
    fh.close()
    for _struct in par.structs:
        print _struct.name, "0x%X"%_struct.getStructSize()
        #print _struct