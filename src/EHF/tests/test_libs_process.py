import unittest

import logging
logger = logging.getLogger(__name__)

from EHF.libs import ehfprocess as process


class TestLibsProcess(unittest.TestCase):
    
    processHelper = process.ProcessHelper()
    
    def test_find_process(self):
        self.assertTrue( self.processHelper.findProcessByName("iw3mp.exe") )
    
    
if __name__ == "__main__":
    unittest.main()