import unittest
from EHF.applications.COD4 import config

class TestEntitiesIw4mp(unittest.TestCase):
    def setUp(self):
        self.appInfo = config.Cod4AppInfo()
        self.envInfo = config.Cod4EnvInfo()
        
    def test_entities_valid(self):
        self.assertTrue(self.appInfo)
        self.assertTrue(self.envInfo)
    
    def test_entities_override(self):
        self.assertEqual(self.appInfo.targetAppWindowClass, "CoD4")
        self.assertEqual(self.appInfo.targetMemStart, 0x00401000)
        self.assertEqual(self.appInfo.targetMemSize, 0x00700000)
        self.assertEqual(self.envInfo.crossHairLineColor, 0xFFFF1111)
        
if __name__ == "__main__":
    unittest.main()