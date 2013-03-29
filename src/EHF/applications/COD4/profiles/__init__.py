def getGunProfiles():
    import guns
    reload(guns)
    return guns.guns
     