import unittest

import os

from EHF.tools import cstructparser

class TestParserOne(unittest.TestCase):
    def setUp(self):
        self.testFile = "testheaderone.h"
        
    def test_readBoundary(self):
        pass
    
    
if __name__ == "__main__":
    unittest.main()