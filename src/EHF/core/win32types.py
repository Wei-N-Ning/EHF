from ctypes import c_int, c_uint
from ctypes import c_short, c_ushort
from ctypes import c_byte, c_ubyte
from ctypes import c_char, c_wchar, c_char_p, c_wchar_p
from ctypes import c_long, c_ulong
from ctypes import c_float, c_double
from ctypes import cast, pointer, POINTER
from ctypes import c_void_p
from ctypes import c_int32, c_uint32
from ctypes import c_int64, c_uint64
from ctypes import c_int16, c_uint16 

from ctypes import byref
from ctypes import sizeof

from ctypes import Structure

from ctypes import WINFUNCTYPE

from ctypes.wintypes import LPCWSTR

WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)

BYTE = c_byte

WCHAR = c_wchar

DOUBLE = c_double

BOOLEAN = BYTE
BOOL = c_long

LPCOLESTR = LPOLESTR = OLESTR = c_wchar_p
LPCWSTR = LPWSTR = c_wchar_p
LPCSTR = LPSTR = c_char_p

HANDLE = c_void_p

UINT = c_uint
INT = c_int

PROCESS_ALL_ACCESS = 0x0010

WS_EX_TOPMOST       = 8
WS_EX_COMPOSITED    = 0x02000000
WS_EX_TRANSPARENT   = 32
WS_EX_LAYERED       = 0x00080000

WS_POPUP            = 0x80000000

WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)