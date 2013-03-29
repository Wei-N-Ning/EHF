import subprocess
import unittest
import time

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

from EHF.libs import ehfprocess as process
from EHF.libs.ehfmemory import reader
from EHF.libs.ehfmemory import scanner
from EHF.libs import ehfmemory

from ctypes import create_string_buffer, byref, sizeof

class TestIw3mp(unittest.TestCase):
    """
    all the tests must be done when iw3mp.exe is running
    """
    
    appName = "iw3mp.exe"
    appWindowClass = "CoD4"
    
    def customSetUp(self):
        pass
    
    def setUp(self):
        """
        fetch the process of iw3mp.exe
        """
        self.ready = False
        self.processHelper = process.ProcessHelper()
        self.processHelper.findWindowByClass(self.appWindowClass)
        self.processHelper.openProcess()
        if self.processHelper.hProcess:
            self.ready = True
            self.memoryReader = reader.MemoryReader(self.processHelper.hProcess)
            self.baseReader = ehfmemory.BaseReader(self.processHelper.hProcess)
        else:
            logger.warning("[TestLibsMemoryIw3mp] Can not find [Call of Duty 4: Modern Warfare Multiplayer] process. All tests are bypassed")
        self.customSetUp()
            

class TestLibsMemoryIw3mp(TestIw3mp):
    def test_find_one_address(self):
        if not self.ready:
            return
        address=0x0043FB20
        self.assertTrue(self.memoryReader.readInt(address))
    
    
class TestBaseReaderIw3mp(TestIw3mp):
    def test_scan_trunk(self):
        if not self.ready:
            return
        buf = create_string_buffer(0x40)
        self.baseReader._rpm(address=0x00400000, buf=buf, length=0x40)
        self.assertTrue(buf.value)


class TestMemoryScannerIw3map(TestIw3mp):
    def customSetUp(self):
        if not self.ready:
            return
        self.memoryScanner = scanner.MemoryScanner(self.processHelper.hProcess,
                                                   0x00401000,
                                                   0x00700000,
                                                   "EHF.applications.COD4.config.PatternFinderRepo")
    
    def test_find_one(self):
        if not self.ready:
            return
        self.memoryScanner.run()
        self.assertTrue(self.memoryScanner.values)
        self.assertEqual(self.memoryScanner.values["CGS"], 0x749888)
        self.assertEqual(self.memoryScanner.values["CG"], 0x74D2B8)
        self.assertEqual(self.memoryScanner.values["Entity"], 0x84E258)
        self.assertEqual(self.memoryScanner.values["ClientInfo"], 0x8381F0)
        
        
        
if __name__ == "__main__":
    unittest.main()