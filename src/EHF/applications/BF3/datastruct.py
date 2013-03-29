from EHF.core.datastruct import *
from EHF.libs import ehfmaths as maths

# DO NOT USE WHEN ITERATE! CALCULATE THE ACTUAL ARRAY SIZE: 
# ( (ptrArrayClientPlayerLast - ptrArrayClientPlayer)/4)
MAXPLAYER = 64


class PtrArrayClientSoldier(Structure):
    
    _fields_ = [
        ("arr",  DWORD * MAXPLAYER)
    ]
    
    
class SimplePlayer(object):
    """
    Holding the esp-friendly player data
    
        CharacterPoseType_Stand,           //0x0          
        CharacterPoseType_Crouch,          //0x1      
        CharacterPoseType_Prone,           //0x2     
        CharacterPoseTypeCount             //0x3   
    """
    def __init__(self):
        self.position = maths.VECTOR3()
        self.teamId = 0
        self.address = 0x0
        self.poseType = 0x0
        self.yaw = 0.0
        
    def initialise(self):
        self.position = maths.VECTOR3()
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
    
    def setPoseType(self, poseType=0):
        self.poseType = poseType
    
    def setYaw(self, yaw):
        self.yaw = yaw
        
    
mockSimplePlayerArgs = \
[ { "posX":  -100.0, "posY": 2.6, "posZ": -87.0, "teamId":0 },
  { "posX":  -43.0, "posY": 2.62, "posZ": -99.0, "teamId":1 },
  { "posX":  -18.0, "posY": 3.12, "posZ": -96.0, "teamId":0 },
  { "posX":  47.0,  "posY": 2.46, "posZ": -41.0, "teamId":1 },
  { "posX":  -10.0, "posY": 2.8, "posZ": -5.0, "teamId":0 },
  { "posX":  -10.0, "posY": 2.8, "posZ": -5.0, "teamId":1 },
  { "posX":  -6.0, "posY": 2.42, "posZ": 4.0, "teamId":0 },
  { "posX":  41.0, "posY": 2.12, "posZ": 0.0, "teamId":1 },
  { "posX":  64.0, "posY": 3.44, "posZ": 16.0, "teamId":0 },
  { "posX":  -46.0, "posY": 3.23, "posZ": 34.0, "teamId":1 },
  { "posX":  78.0, "posY": 3.04, "posZ": 54.0, "teamId":0 },
]

def setPlayerMockAttr(_player, mockArgs):
    _player.setAddress(0xFFFFFFFF)
    _player.setTeamId( mockArgs.get("teamId", 0) )
    _player.setPositionN( mockArgs.get("posX", 0.0), 
                          mockArgs.get("posY", 0.0),
                          mockArgs.get("posZ", 0.0) )
    
