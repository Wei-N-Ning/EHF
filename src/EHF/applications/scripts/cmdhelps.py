from EHF.core import win32types
from EHF.libs import ehfmaths
import ctypes
import struct
import sys
import os
import cPickle

def iterPrimaryVars(parser):
    if not parser.appInfo.primaryVars:
        print "Application has no primary variable!!"
        return
    for k in sorted(parser.appInfo.primaryVars.keys()):
        v = parser.appInfo.primaryVars[k]
        if isinstance(v, int) or isinstance(v, long):
            print k, "0x%X"%v 
        else:
            print k, v

ipv = iterPrimaryVars


class __MemDump256(ctypes.Structure):
    _fields_ = [ ("arr", win32types.DWORD * 256) ]

class __MemDump256F(ctypes.Structure):
    _fields_ = [ ("arr", win32types.c_float * 256) ]


def saveOrAppendData(data):
    fileName = "D:\\ProWIP\\Programming\\dev\\python\\EHFPROJECT\\src\\EHF\\applications\\scripts\\temp\\log.dat"
    fh = None
    oldData = []
    if os.path.exists(fileName):
        fh = open(fileName, "r")
        oldData = cPickle.load(fh)
        fh.close()
    oldData.append(data)
    fh = open(fileName, "w")
    cPickle.dump(oldData, fh)
    fh.close()
    print "WRITE DONE!!!"
    
def logm(parser, address):
    """
    log the 4x4 matrix data structure starting at the given address
    save the resulting list to temp file (append)
    """
    mat = ehfmaths.MATRIX44()
    application = parser.application
    prmVar = application._attributes["AppInfo"].primaryVars
    address = prmVar["GameRenderer"] + address
    mr = application._attributes["MemoryReader"]
    mr._rpm(address, mat, 64)
    data = [entry for entry in mat.arr]
    saveOrAppendData(data)

def rpmf(parser, prmVar, format=8):
    """
    the size of each segment is 0x8 bytes
    the size of each line is 0x20 bytes 
    
    fixed 1024 bytes dump...
    """
    __rpmFCache = getattr(parser, "_rpmFCache", [0.0]*256)
    __rpmFCacheAssigned = getattr(parser, "_rpmFCacheAssigned", False)
    application = parser.application
    appInfo = parser.appInfo
    mr = application._attributes["MemoryReader"]
    _value = __MemDump256F()
    offset = 0x0
    if '+' in prmVar:
        prmVar, offset = prmVar.split('+')
        offset = int(offset, 16)
    elif '-' in prmVar:
        prmVar, offset = prmVar.split('-')
        offset = 0 - int(offset, 16)
    elif prmVar.startswith("0x"):
        prmVar, offset = "__", int(prmVar, 16)
    mr._rpm(appInfo.primaryVars.get(prmVar, 0x0)+offset, _value, ctypes.sizeof(_value))
    _printable = []
    for idx in range(0, 256):
        _v = _value.arr[idx]
        if abs(_v) < 0.0001:
            _v = "0.0"
        elif abs(_v) > 9999:
            _v = "inf"
        else:
            _v = "%.4f" % _v
        # check if changed
        _ov = _v
        if __rpmFCacheAssigned:
            if _v != __rpmFCache[idx]:
                _v = "{%s}" % _v
        __rpmFCache[idx] = _ov
        #
        _v = _v.rjust(10)
        if idx and idx % format == 0:
            _v = '\n'+_v
        _printable.append(_v)
    __rpmFCacheAssigned = True
    parser._rpmFCache = __rpmFCache
    parser._rpmFCacheAssigned = __rpmFCacheAssigned
    print ''.join(_printable)

def rpm(parser, prmVar, format=8):
    """
    fixed 1024 bytes dump...
    """
    __rpmCache = getattr(parser, "_rpmCache", [0]*256)
    __rpmCacheAssigned = getattr(parser, "_rpmCacheAssigned", False)
    application = parser.application
    appInfo = parser.appInfo
    mr = application._attributes["MemoryReader"]
    _value = __MemDump256()
    offset = 0x0
    if '+' in prmVar:
        prmVar, offset = prmVar.split('+')
        offset = int(offset, 16)
    elif '-' in prmVar:
        prmVar, offset = prmVar.split('-')
        offset = 0 - int(offset, 16)
    elif prmVar.startswith("0x"):
        prmVar, offset = "__", int(prmVar, 16)
    mr._rpm(appInfo.primaryVars.get(prmVar, 0x0)+offset, _value, ctypes.sizeof(_value))
    _printable = []
    for idx in range(0, 256):
        _v = "%08X" % _value.arr[idx]
        # check if changed
        _ov = _v
        if __rpmCacheAssigned:
            if _v != __rpmCache[idx]:
                _v = "{%s}" % _v
        __rpmCache[idx] = _ov
        #
        _v = _v.rjust(12)
        if idx and idx % format == 0:
            _v = '\n'+_v
        _printable.append(_v)
    __rpmCacheAssigned = True
    parser._rpmCache = __rpmCache
    parser._rpmCacheAssigned = __rpmCacheAssigned
    print ''.join(_printable)


def printh(value, label=''):
    print label + "0x%X" % value


def vel(parser):
    """
    A bf4 helper function to inspect the vehicle data block from the local player
    """
    application = parser.application
    appInfo = parser.appInfo
    mr = application._attributes["MemoryReader"]
    localPlayerAddress = appInfo.primaryVars["LocalPlayerAddress"]
    int64 = ctypes.c_ulonglong()
    mr._rpm(localPlayerAddress+0xDB0, int64, 8)
    vehicleDataBlock = int64.value
    printh(vehicleDataBlock, "VehicleDataBlock: ")
    mr._rpm(vehicleDataBlock+0x238, int64, 8)
    vehEntity = int64.value
    printh(vehEntity, "VehicleEntity: ")
    rpmf(parser, "0x%X" % (vehEntity+0x200))
    
    
def findmx(parser, prmVar):
    pass

def getVars(parser):
    return parser.appInfo.vars