def getClass(modulePath, className):
    mdl = None
    try:
        mdl = __import__(modulePath, fromlist=modulePath.split('.')[1:])
    except ImportError, e:
        print e
        return None
    return getattr(mdl, className, None)