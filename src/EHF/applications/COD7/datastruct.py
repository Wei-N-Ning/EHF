from EHF.core.datastruct import *
from EHF.libs import ehfmaths as maths

PLAYERMAX = 32            # number of players to loop in
ENTITIESMAX = 1024        # total number of entities present XXX
AMMOMAX = 16              # number of ammo slots in CG_T
RCXDMAX = 16
DOGSMAX = 16

class COD7_RefDef(Structure):
    _fields_ = [ 
                 ("viewAngles", maths.VECTOR),    # 0x00
                 ("_buf", c_char * 0x14C),  
                 ("x", c_int),              # 0x00
                 ("y", c_int),              # 0x04
                 ("width", c_int),          # 0x08
                 ("height", c_int),         # 0x0C
                 ("fov_x", c_float),        # 0x10
                 ("fov_y", c_float),        # 0x14
                 ("totalfov", c_float),     # 0x18
                 ("viewOrg", maths.VECTOR),       # 0x1C
                 ("other", c_int),      # 0x28
                 ("viewAxis", maths.VECTOR * 3),  # 0x2C
                 ]
    
    
class COD7_Ammo(Structure):
    _fields_ = [ ("weapon_id", c_int),          # 0x00
                 ("ammo", c_int),               # 0x04
               ]                                # 0x08
    

class COD7_CG_T(Structure):
    _fields_ = [ ("clientNum", c_int),          # 0x00
                 ("_p00", c_char * 32),         # 0x04
                 ("time", c_int),               # 0x24
                 ("snap", c_int),               # 0x28
                 ("nextSnap", c_int),           # 0x2C
                 ("_p01", c_char * 84),         # 0x30
                 ("ping", c_int),               # 0x84
                 ("_p02", c_char * 44),         # 0x88
                 ("lerpOrigin", maths.VECTOR),        # 0xB4
                 ("newOrigin", maths.VECTOR),         # 0xC0
                 ("_p03", c_char * 16),         # 0xCC
                 ("zoomTime", c_int),           # 0xDC
                 ("_p04", c_char * 244),        # 0xE0
                 ("weapon", c_int),             # 0x1D4
                 ("_p05", c_char * 16),         # 0x1E4
                 ("state", c_int),              # 0x1E8    1:3:4:Switching Weapon; 6:Shooting; 12:Reload Start; 10:Reloading; 14:Reload End; 27:Sprint Start; 28:Sprinting; 29:Sprint End
                 ("isClimbing", c_int),         # 0x1EC    4:Climbing
                 ("_p06", c_char * 8),          # 0x1F0
                 ("isZoomed", c_float),         # 0x1F8
                 ("_p07", c_char * 20),         # 0x1FC
                 ("viewAngleY", c_float),       # 0x210
                 ("viewAngleX", c_float),       # 0x214
                 ("_p09", c_char * 560),        # 0x218
                 ("ammos", COD7_Ammo * AMMOMAX),# 0x448
                 ]                              # 0x490
    
    
class COD7_SNAPSHOT_T(Structure):
    _fields_ = [ ("snapFlags", c_int),          # 0x00
                 ("ping", c_int),               # 0x04
                 ("serverTime", c_int),         # 0x08
                 ("_p00", c_char * 16),         # 0x0C
                 ("isReloading", c_int),        # 0x1C
                 ("_p01", c_char * 20),         # 0x20
                 ("viewOrg", maths.VECTOR),           # 0x34
                 ("deltaX", c_float),           # 0x40
                 ("deltaY", c_float),           # 0x44
#                 ("_p02", c_char * 168),        # 0x48
#                 ("stance", c_int),             # 0xF0 0:Standing; 4:Crouching; 8:Prone;
#                 ("_p03", c_char * 264),        # 0xF4
                ] 
    

class COD7_CGS_T(Structure):
    _fields_ = [ ("_p00", c_char * 32),         # 0x00
                 ("gamemode", c_char * 4),      # 0x20
                 ("_p01", c_char * 28),         # 0x24
                 ("server", STR16),             # 0x40
                 ("_p02", c_char * 244),        # 0x50
                 ("map", c_char * 32),          # 0x144
                ]


class COD7_ClientInfo_T(Structure):
    _fields_= [ ("infoValid", c_int),   # 0x000
                ("infoValid2", c_int),  # 0x004
                ("index", c_int),       # 0x008
                ("name", STR32),        # 0x00C
                ("team", c_int),        # 0x02C
                ("team2", c_int),       # 0x030
                ("_p02", c_char * 4),   # 0x034
                ("rank", c_int),        # 0x038
                ("_p03", c_char * 52),  # 0x03C
                ("kills", c_int),       # 0x070
                ("assist", c_int),      # 0x074
                ("deaths", c_int),      # 0x078
                ("_p09", c_char * 976), # 0x07C
                ("anglex", c_float),    # 0x44C
                ("angley", c_float),    # 0x450
                ("_p04", c_char * 168), # 0x454
                ("pose", c_int),        # 0x4FC
                ("_p05", c_char * 4),   # 0x500
                ("isshooting", c_int),  # 0x504
                ("iszoomed", c_int),    # 0x508
                ("_p06", c_char * 44),  # 0x50C
                ("weapon", c_int),      # 0x538
                ("_p07", c_char * 148), # 0x53C
               ]                        # 0x5C8


class COD7_Entity_T(Structure):
    _fields_= [ ("_p00", c_char * 48),      # 0x000
                ("pos", maths.VECTOR),            # 0x030
                ("anglex", c_float),        # 0x03C
                ("angley", c_float),        # 0x040
                ("anglez", c_float),        # 0x044
                ("_p01", c_char * 320),     # 0x048
                ("newpos", maths.VECTOR),         # 0x188
                ("_p02", c_char * 24),      # 0x194
                ("angle2", maths.VECTOR),         # 0x1AC
                ("_p12", c_char * 48),      # 0x1B8
                ("clientnum", c_int),       # 0x1E9
                ("pose", c_int),            # 0x1EC 0:Not Zoomed 0x40000 stealth perk?
                ("_p22", c_char * 16),      # 0x1F0
                ("oldpos", maths.VECTOR),         # 0x200
                ("_p03", c_char * 24),      # 0x20C
                ("oldangle", maths.VECTOR),       # 0x224
                ("_p13", c_char * 20),      # 0x230
                ("movingState", c_int),     # 0x244 1:Standing Still; 3:Prone or ADS Moving; 4:Walking; 7:Running
                ("weaponId", c_int),        # 0x248
                ("_p23", c_char * 90),      # 0x24C    
                ("type", c_short),          # 0x2A6
                ("_p04", c_char * 10),      # 0x2A8
                ("weapon", c_short),        # 0x2B2
                ("_p14", c_char * 112),     # 0x2B4
                ("alive", c_ubyte),         # 0x324
                ("isalive2", c_ubyte),      # 0x325
                ("_p05", c_char * 2),       # 0x326
                ]   
    

class COD7_ClientInfo(Structure):
    _fields_ = [ ("arr", COD7_ClientInfo_T * PLAYERMAX) ]


class COD7_Entity(Structure):
    _fields_ = [ ("arr", COD7_Entity_T * ENTITIESMAX) ]


class COD7_WeaponDesc_T(Structure):
    _fields_ = [ ("model", c_int),          # 0x00
                 ("i1", c_int),             # 0x04
                 ("i2", c_int),             # 0x08
                 ("name_addr", c_int),      # 0x0C
                 ("_p99", c_char * 0xD4),   # 0x10
                 ]                          # 0xE4

class COD7_WeaponDesc(Structure):
    _fields_ = [ ("arr", c_int * 2048)]


class COD7_RCXD_T(Structure):
    _fields_ = [ ("client_num", c_int),     # 0x00
                 ("i1", c_int),             # 0x04
                 ("pos", maths.VECTOR),           # 0x08
                 ("team", c_int),           # 0x14
                 ("owner", c_int),          # 0x18
                 ]                          # 0x1C

class COD7_RCXD(Structure):
    _fields_ = [ ("arr", COD7_RCXD_T * RCXDMAX) ]


class COD7_DOG_T(Structure):
    _fields_ = [ ("client_num", c_int),     # 0x00
                 ("i1", c_int),             # 0x04
                 ("pos", maths.VECTOR),           # 0x08
                 ("team", c_int),           # 0x14
                 ("owner", c_int),          # 0x18
                 ("i2", c_int),             # 0x1C
                 ]                          # 0x20

class COD7_DOG(Structure):
    _fields_ = [ ("arr", COD7_DOG_T * DOGSMAX) ]
    


class Player(object):
    """
    a COD7 player class
    """
    def __init__(self):
        self.valid = 0
        self.pos = None
        self.newpos = None
        self.oldpos = None
        self.prev_pos = None
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        self.client_num = 0
        self.type = 0
        self.pose = 0
        self.shooting = 0
        self.zoomed = 0
        self.weapon_num = 0
        self.alive = 0
        self.enemy = False

        self.name = ""
        self.team = 0
        self.perk = 0
        
        self.color_esp = 0
        self.color_map = 0
        self.motion = maths.VECTOR(0, 0, 0)               # motion vector of the player, in game units per second
        
        self.entity = None
        self.client_info = None
        
        self.aimbot = True                      # this entity is eligible for aimbot

    def set_values(self, cod7_entity, cod7_clientinfo):
        self.entity = cod7_entity
        self.client_info = cod7_clientinfo
        #self.valid = cod7_entity.valid
        self.valid = True
        self.prev_pos = self.pos
        self.pos = cod7_entity.pos
        self.newpos = cod7_entity.newpos
        self.oldpos = cod7_entity.oldpos
        self.pitch = cod7_entity.anglex
        self.yaw = cod7_entity.angley
        #self.roll = cod7_entity.fRoll
        #self.client_num = cod7_entity.clientNum
        self.type = cod7_entity.type
        #self.shooting = cod7_entity.Shooting
        #self.zoomed = cod7_entity.Zoomed
        self.weapon_num = cod7_entity.weapon
        self.alive = cod7_entity.alive
        
        p_str = cast(pointer(cod7_clientinfo.name), c_char_p)
        self.name = p_str.value
        self.team = cod7_clientinfo.team
        self.pose = cod7_entity.pose
        self.perk = 0
        

class EntityTracker(object):
    """
    a COD7 entity track class
    """
    def __init__(self, idx):
        self.idx = idx                      # index of entity object
        self.startoflife = -1               # time_code when the entity was first tracked
        self.endoflife = -1                 # time_code when the object will not exist anymore
        self.pos = maths.VECTOR()                 # position
        self.yaw = 0
        self.type = 0                       # type of object (as in entity)
        self.alive = 0                      # alive attribute (as in entity)
        self.weapon_num = 0                 # weaponnum (as in entity)
        self.model_name = ""                # model name
        self.planter = None                 # player who planted the explosive
        self.enemy = True                   # is entity enemy? 
        
        # following attributes mimick player attributes to make it aimbotable
        self.aimbot = False                 # not eligible for aimbot by dfault
        self.valid = True
        self.pose = 0                           # standard standing
        self.newpos = maths.VECTOR()
        self.oldpos = maths.VECTOR()
    
    def set_values(self, cod7_entity):
        self.pos = cod7_entity.pos
        self.oldpos = cod7_entity.oldpos
        self.newpos = cod7_entity.newpos
        self.yaw = cod7_entity.angley
        self.type = cod7_entity.type
        self.alive = cod7_entity.alive
        self.weapon_num = cod7_entity.weapon