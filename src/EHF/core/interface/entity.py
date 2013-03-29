class BaseAddressEntry(object):
    """
    is a high level wrapper on top of a binary address,
    it has value, address, length and expectedValue
    the type class attribute is used to identify its usage
    
    rawValue: is always string, 
    """
    
    _dataTypes = {
                    "pad byte":'x',          
                    "char":'c',     
                    "signed char":'b',
                    "unsigned char":'B',
                    "_Bool":'?',
                    "short":'h',
                    "unsigned short":'H',
                    "int":'i',
                    "unsigned int":'I',
                    "long":'l',
                    "unsigned long":'L',
                    "long long":'q',
                    "unsigned long long":'Q',
                    "float":'f',
                    "double":'d',
                    "char[]":'s',          
                    "char[]":'p',          
                    "void *":'P'
                 }
    
    def __init__(self, 
                 label="AddressEntry", 
                 dataType="int", 
                 address=0x0, 
                 length=4, 
                 initValue=0, 
                 expectedValue=0):
        self.label = label
        self.dataType = dataType
        self.rawValue = ""
        self.value = initValue
        self.address = address
        self.length = length
        self.expectedValue = expectedValue
    
    def __repr__(self):
        return "[%s] 0x%x (0x%x bytes): %s" % (self.label, self.address, self.length, str(self.value))
    
    def __str__(self):
        return self.__repr__()


class BaseDataEntry(object):
    """
    is a high level wrapper similar to a structure,
    it has fields (attributes)
    
    it could represent as complex as a game session (hundreds of attributes),
    or as simple as a float3<> array
    """
    type = ""
    
    def __init__(self):
        pass
