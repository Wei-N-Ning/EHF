"""
graphics related classes, functions
"""

from ctypes.wintypes import DWORD, LONG, ULONG, WORD, string_at, byref, Structure, Union, POINTER, sizeof, windll
from directx.types import D3DXVECTOR2
from directx.d3dx import RECT

from ctypes import cast

from math import radians, cos, sin, ceil

DT_TOP                      = 0x00000000
DT_LEFT                     = 0x00000000
DT_CENTER                   = 0x00000001
DT_RIGHT                    = 0x00000002
DT_VCENTER                  = 0x00000004
DT_BOTTOM                   = 0x00000008
DT_WORDBREAK                = 0x00000010
DT_SINGLELINE               = 0x00000020
DT_EXPANDTABS               = 0x00000040
DT_TABSTOP                  = 0x00000080
DT_NOCLIP                   = 0x00000100
DT_EXTERNALLEADING          = 0x00000200
DT_CALCRECT                 = 0x00000400
DT_NOPREFIX                 = 0x00000800
DT_INTERNAL                 = 0x00001000


LP_D3DXVECTOR2 = POINTER(D3DXVECTOR2)


def draw2DViewFrustum(line, forwardVec, x, y, color):
    """
    draw the 2d view frustum
    """
    pass