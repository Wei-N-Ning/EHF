from EHF.core.datastruct import *
from EHF.libs import ehfmaths as maths
from EHF.libs.ehfmaths import types as ehfmaths_types
from EHF.libs.ehfmaths import functions as ehfmaths_functions

PLAYERMAX = 32            # number of players to loop in
ENTITIESMAX = 1024        # total number of entities present XXX
AMMOMAX = 16              # number of ammo slots in CG_T

ET_PLAYER           = 1


class RefDef(Structure):
    _fields_ = [
    ]


class ClientInfo(Structure):
    _fields_ = [ 
    ]
    

class ClientInfoArray(Structure):
    _fields_ = [ ("arr",   ClientInfo * PLAYERMAX) ]    



class Entity(Structure):
    """
    size = 0x31C
    """
    _fields_ = [
       ("_unknown01",  c_char * 24), # 0x0
       ("position",    ehfmaths_types.VECTOR), # 0x18
       ("yaw",  c_float), # 0x3C
       ("pitch", c_float), # 0x40
       ("_unknown02",  c_char * 0x2D8) # 0x44
    ]
    
    
class EntityArray(Structure):
    _fields_ = [ ("arr",   Entity * PLAYERMAX) ]


class CG(Structure):
    _fields_ = [
    ]    


class CGS(Structure):
    _fields_ = [
    ]