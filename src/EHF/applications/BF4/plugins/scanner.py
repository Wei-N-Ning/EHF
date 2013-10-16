from EHF.plugins.common import memory
from EHF.libs.ehfmemory import scanner


class BF4ScannerPlugin(memory.MemoryScannerPlugin):
    """
    Dump and scan the target process memory for certain bit patterns.
    """
    def initialise(self):
        self.scn = scanner.MemoryScanner(self._appAttr["ProcessHelper"].hProcess,
                                         self._appAttr["AppInfo"].targetMemStart,
                                         self._appAttr["AppInfo"].targetMemSize,
                                         "EHF.applications.BF4.config.PatternFinderRepo",
                                         is64Bit=True)
        
    def _run(self):
        self.scn.run()
        if self.scn.values and self.scn.bases:
            for pfLabel in self.scn.values:
                offset = self.scn.values[pfLabel]
                baseAddress = self.scn.bases[pfLabel]
                self._appAttr["AppInfo"].primaryVars[pfLabel] = offset + baseAddress