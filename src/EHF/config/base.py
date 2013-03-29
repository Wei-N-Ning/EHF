class BaseConfig(object):
    
    def __init__(self):
        self._configDict = {
                            "global_FPS"           : 60.0,
                             
                           }
        
    def addConfig(self, key, value):
        self._configDict[key] = value
    
    def getConfig(self, key, defaultValue=None):
        return self._configDict.get(key, defaultValue)
    
    def getRequirements(self):
        """
        requirements is a subset of config,
        the contents need to be checked against a set of hardcoded value to
        ensure the application will function as expected.
        the requirement entries must start with rq_$$ where $$ is the number
        of the requirement entry
        """
        _requirements = {}
        for k,v in self._configDict.values():
            if k.startswith("rq_"):
                _requirements[k] = v
        return _requirements