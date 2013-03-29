import unittest

from EHF.core import application
from EHF.plugins import base

import logging
logging.root.setLevel(logging.INFO)

class MockApplication(application.BaseApplication):
    pluginDefinitions = [
                         ("EHF.tests.test_application", "MockPluginUpper"),
                         ("EHF.tests.test_application", "MockPluginLower")
                        ]

class MockPluginUpper(base.BasePlugin):
    uid = 0x1
    requirements = []
    contributions = ["rice", "meat"]

class MockPluginLower(base.BasePlugin):
    uid = 0x2
    requirements = ["rice", "meat"]
    contributions = ["sushi", "friedRice"]
    
    
class TestApplication(unittest.TestCase):
    def test_application_plugin_registry(self):
        mockApp = MockApplication()
        self.assertEqual(
                         [x.uid for x in mockApp.getPlugins()], 
                         [0x1, 0x2]
                        )
    
    def test_appliction_execution(self):
        mockApp = MockApplication(debug=True, debugTicks=50)
        mockApp.execute()
        
        
if __name__ == "__main__":
    unittest.main()