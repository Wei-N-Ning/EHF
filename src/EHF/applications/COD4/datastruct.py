from EHF.core.datastruct import *
from EHF.libs import ehfmaths as maths

PLAYERMAX = 32            # number of players to loop in
ENTITIESMAX = 1024        # total number of entities present XXX
AMMOMAX = 16              # number of ammo slots in CG_T

ET_PLAYER           = 1

# game_modes
# dm= Free for all
# sab= Sabotage
# war= Team Death Match
# dom= Domination
# dd= Demolition
# koth= HQ
# sd= Search & Destroy
# ctf= Catch the flag

# team
# 1, 2
# 3: speculator

# CG = ClientGame
# CGS = ClientGameServer

"""
typedef struct 
{
       int  x;
       int  y;
       int  width;
       int  height;
     float  fov_x;
     float  fov_y;
    vec3_t    vieworg;
    vec3_t    viewaxis[3];
      char  _p00[0x4050];
    vec3_t    refdefViewAngles;
}refdef_t;
"""
class RefDef(Structure):
    _fields_ = [
        ("x",                  c_int), # 0x0000
        ("y",                  c_int), # 0x0004
        ("width",              c_int), # 0x0008
        ("height",             c_int), # 0x000c
        ("fov_x",            c_float), # 0x0010
        ("fov_y",            c_float), # 0x0014
        ("viewOrigin",  maths.VECTOR), # 0x0018
        ("viewAxis",  maths.VECTOR*3), # 0x0024
        ("_unknown",   c_char*0x4050), #
        ("refDefViewAngles", maths.VECTOR), 
    ]


class ClientInfo(Structure):
    _fields_ = [ 
        ("infoValid",          c_int), # 0x0000    1
        ("_unknown01",         c_int), # 0x0004
        ("clientNum",          c_int), # 0x0008    0
        ("Name",           c_char*16), # 0x000C
        ("Team",               c_int), # 0x001C    2,3
        ("Team2",              c_int), # 0x0020    2,3
        ("Rank",               c_int), # 0x0024    0
        ("_unknown02",     c_char*20), # 0x0028 
        ("bodyModel",      c_char*64), # 0x003C    body_mp_sas_urban_assault
        ("headModel",      c_char*64), # 0x007C    weapon_m16gr_sp
        ("_unknownXX",     c_char*1040),
#        ("weapModel",      c_char*64), # 0x00BC
#        ("weaponModel",    c_char*26),
#        ("_unknown03",    c_char*320),
#        ("model",          c_char*64),
#        ("_unknown04",    c_char*284),
#        ("posX",             c_float),
#        ("posY",             c_float),
#        ("posZ",             c_float),
#        ("_unknown05",      c_char*8),
#        ("yaw",              c_float),
#        ("roll",             c_float),
#        ("pitch",            c_float),
#        ("_unknown06",    c_char*208),
#        ("shooting",           c_int),
#        ("_unknown07",      c_char*4),
#        ("zoomed",             c_int),
#        ("_unknown08",   c_char*0x18),
#        ("iWeaponID",          c_int),
#        ("_unknown09",   c_char*0x1C),
    ]
    

# loop-able, indexed by clientNum
class ClientInfoArray(Structure):
    _fields_ = [ ("arr",   ClientInfo * PLAYERMAX) ]    


"""
class Entity
{
public:
    __int32 isValid; //0x0000 
char _0x0004[24];
    float posX; //0x001C 
    float posY; //0x0020 
    float posZ; //0x0024 
    float rotX; //0x0028 
    float rotY; //0x002C 
    float rotZ; //0x0030 
char _0x0034[48];
    BYTE movingSta; //0x0064 
    BYTE N0086EF5F; //0x0065 
    BYTE isAds; //0x0066 
char _0x0067[13];
    float pos2X; //0x0074 
    float pos2Y; //0x0078 
    float pos2Z; //0x007C 
char _0x0080[84];
    BYTE movingStO; //0x00D4 
    BYTE N0088542D; //0x00D5 
    BYTE isAdsO; //0x00D6 
    BYTE N0088542E; //0x00D7 
char _0x00D8[812];

};//Size=0x0404
"""
class Entity(Structure):
    _fields_ = [
#        ("_unknown01",             c_char*2), #0x0000
#        ("isValid",             c_byte), #0x0002    1
#        ("_unknown02",            c_char*25), #0x0003
#        ("lerpOrigin",         maths.VECTOR), #0x001C    -339.051849365
#                                              #          -567.769226074
#                                              #          200.258926392
#        ("lerpAngles",         maths.VECTOR), #0x0028    9.40979003906
#                                              #          88.7585449219
#                                              #          0.0
#        ("_unknown02",            c_char*48), #0x0034
#        ("dwEntState",                DWORD),
#        ("_unknown02c",          c_char*0xC),
#        
#        ("oldLocation",        maths.VECTOR), #0x0074
#        ("_unknown02b",           c_char*76),
#        ("clientNum",                 c_int), #0x00CC    0
#        ("entityType",                DWORD), #0x00D0    1 (important!!)
#        ("eFlags",                    DWORD), #0x00D4    4 (0 if dead)
#        ("unknown02a",            c_char*12),
#        ("newLocation",        maths.VECTOR),
#        ("_unknown03",           c_char*184), #0x00D8
#        ("weapon",                    c_int), #0x0190    32 (m16+m203)
#        ("_unknown04",            c_char*44), #0x0194
#        ("isAlive",                   c_int), #0x01C0
#        ("_unknown05",            c_char*24), #0x01C4    1 (0 if dead)

        ("isValid",               c_int), #0x0000
        ("_unknown01",      c_char*0x18), #0x0004
        ("location",       maths.VECTOR), #0x001C
        ("rotation",       maths.VECTOR), #0x0028
        ("_unknown02",      c_char*0x30),
        ("dwEntState",            DWORD),
        ("_unknown03",      c_char*0x0C),
        ("oldLocation",    maths.VECTOR), #0x0074
        ("_unknown04",      c_char*0x4C),
        ("clientNum",             c_int), #0x00CC
        ("entityType",            c_int), #0x00D0
        ("_unknown05",      c_char*0x10),
        ("newLocation",    maths.VECTOR), #0x00E4
        ("_unknown06",      c_char*0xD0),
        ("isAlive",               c_int), #0x01C0
        ("_unknown07",      c_char*0x18), #0x01C4
    ]
    
    
# loop-able, indexed by clientNum
class EntityArray(Structure):
    _fields_ = [ ("arr",   Entity * PLAYERMAX) ]


"""
typedef struct
{
    int             clientNum;                  4
    int             _p00[0x1C];                 4
    Snapshot_t      *pSnap;                     4
    Snapshot_t      *pNextSnap;                 4
    char            _p01[0x46100];              1
    int             Time;                       4
    char            _p02[0x307C];               1
    vec3_t            RefdefViewAngles;         12
    char            _p03[0x114];                1
    refdef_t        refdef;                     
    char            _p04[0x2F8C];
    int             CrosshairClientNum;
    int             CrosshairClientTime;
}cg_t;
"""
class CG(Structure):
    """
    ClientGame
    """
    _fields_ = [
        ("clientNum",           c_int),    # 0x0000    0
        ("_unknown01",        c_char*40),
        ("Time",              c_int),
        ("crosshairClientNum", c_int),
        ("crosshairCientTime", c_int),
    ]    


class CGS(Structure):
    """
    ClientGameServer
    """
    _fields_ = [
        ("_unknown01",        c_char*8), #0x0000    
        ("scrWidth",             c_int), #0x0008    1280
        ("scrHeight",            c_int), #0x000C    720
        ("_unknown02",       c_char*16), #0x0010
        ("gameType",          c_char*4), #0x0020    war (see above for full list)
        ("_unknown03",       c_char*28), #0x0024
        ("serverName",      c_char*256), #0x0040    CoD4Host
        ("maxPlayers",           c_int), #0x0140    24
        ("mapName",          c_char*64), #0x0144    maps/mp/mp_shipment.d3dbsp
    ]