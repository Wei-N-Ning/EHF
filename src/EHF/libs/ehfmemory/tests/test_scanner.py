from EHF.libs.ehfmemory import scanner


def dryrun_iw3mp():
    from EHF.libs import ehfprocess
    ph = ehfprocess.ProcessHelper()
    ph.findWindowByClass("CoD4")
    ph.openProcess()
    ms = scanner.MemoryScanner(ph.hProcess, 0x00401000, 0x00700000,
                               "EHF.applications.COD4.config.PatternFinderRepo")
    ms.run()
    print ms.valuesToString()
    from EHF.applications.COD4 import datastruct
    refDefInstance = datastruct.RefDef()
    ms._rpm(ms.values["CG"]+0x492c8, refDefInstance, datastruct.sizeof(refDefInstance))
    print "0x%X"%(ms.values["CG"]+0x492c8), refDefInstance.width, refDefInstance.height
    

def dryrun_mohw():
    from EHF.libs import ehfprocess
    ph = ehfprocess.ProcessHelper()