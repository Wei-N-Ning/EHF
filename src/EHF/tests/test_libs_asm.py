import unittest
from EHF.libs.ehfasm import typeconv

class TestLibsAsm(unittest.TestCase):
    
    def test_float_to_hex(self):
        floatValue = 6.66
        self.assertEqual(typeconv.floatToHex(floatValue) , 0x40D51EB8)
    
    def test_hex_to_float(self):
        hexValue = 0x40D51EB8
        self.assertAlmostEqual(typeconv.hexToFloat(hexValue), 6.66, places=6)
    
    
    
if __name__ == "__main__":
    unittest.main()