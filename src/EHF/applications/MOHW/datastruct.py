from EHF.core.datastruct import *
from EHF.libs import ehfmaths as maths

# DO NOT USE, USE (ptrArrayClientPlayerLast - ptrArrayClientPlayer / 4)
MAXPLAYER = 64


class PtrArrayClientSoldier(Structure):
    
    _fields_ = [
        ("arr",  DWORD * MAXPLAYER)
    ]
    
    
class SimplePlayer(object):
    """
    Holding the esp-friendly player data
    """
    def __init__(self):
        self.position = maths.VECTOR3()
        self.viewDirection = maths.VECTOR3()
        self.teamId = 0
        self.address = 0x0
        
    def initialise(self):
        self.position = maths.VECTOR3()
        self.viewDirection = maths.VECTOR3()
        self.teamId = 0
        self.address = 0x0
        
    def setPosition(self, posVec):
        self.position.x = posVec.x
        self.position.y = posVec.y
        self.position.z = posVec.z
        
    def setPositionN(self, x, y, z):
        self.position.x = x
        self.position.y = y
        self.position.z = z
        
    def setTeamId(self, teamId):
        self.teamId = teamId
        
    def setAddress(self, address):
        self.address = address
        
mockSimplePlayerArgs = \
[ { "posX":  -10.0, "posY": 94.6, "posZ": -37.0, "teamId":0 },
  { "posX":  -43.0, "posY": 94.62, "posZ": -49.0, "teamId":1 },
  { "posX":  -18.0, "posY": 95.12, "posZ": -56.0, "teamId":0 },
  { "posX":  47.0,  "posY": 94.46, "posZ": -41.0, "teamId":1 },
  { "posX":  -10.0, "posY": 94.8, "posZ": -5.0, "teamId":0 },
  { "posX":  -10.0, "posY": 94.8, "posZ": -5.0, "teamId":1 },
  { "posX":  -6.0, "posY": 94.42, "posZ": 4.0, "teamId":0 },
  { "posX":  41.0, "posY": 94.12, "posZ": 0.0, "teamId":1 },
  { "posX":  64.0, "posY": 96.44, "posZ": 16.0, "teamId":0 },
  { "posX":  -46.0, "posY": 95.23, "posZ": 34.0, "teamId":1 },
  { "posX":  38.0, "posY": 95.04, "posZ": 54.0, "teamId":0 },
]



def setPlayerMockAttr(_player, mockArgs):
    _player.setAddress(0xFFFFFFFF)
    _player.setTeamId( mockArgs.get("teamId", 0) )
    _player.setPositionN( mockArgs.get("posX", 0.0), 
                          mockArgs.get("posY", 0.0),
                          mockArgs.get("posZ", 0.0) )