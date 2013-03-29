"""
NOTE! float to hex (and hex to float) only guarantee UP-TO 6 places of decimal precision! 

x.xxxxxx

"""

import struct

def hexToFloat(hexValue=0x0):
    """
    give an hex value, perform the reverse of the IEEE single-precision
    floating point conversion and return the decimal floating point value
    
    note that, comparing to asm result, the floating point value produced
    only has upto 7 fraction precision even though python tries to make up
    to the double-precious float
    """
    bitMask = 0x80000000
    
    # the sign bit, left-most
    sign = hexValue & bitMask
    bitMask = bitMask >> 1
    
    # next: the exponent bits, 8 from the left
    expo = 0
    for i in range(8):
        _bit = 1 if (hexValue & bitMask) else 0
        expo += _bit * pow(2, (7 - i) )
        bitMask = bitMask >> 1
    expo -= 127
    
    # next: the 23 fraction bits (plus the "hidden" leading bit that 
    # always equals to 1)
    frac = 0
    for i in range(1, 25):
        _bit = 1 if (hexValue & bitMask) else 0
        frac += _bit * pow(2, -(i))
        bitMask = bitMask >> 1
    result = pow(2, expo) * (1.0 + frac)
    if sign:
        result *= -1
    
    return result

h2f = hexToFloat

def floatToHex(floatValue=0.0):
    return  struct.unpack('i', struct.pack('f', floatValue))[0]

f2h = floatToHex