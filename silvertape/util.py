from os import getenv, environ


class _Env:
    def __init__(self):
        pass
    
    def __getattr__(self, item):
        return getenv(item)
    
    def __setattr__(self, key, value):
        environ[key] =  value
        
    def __delattr__(self, item):
        del environ[item]
        

class _SingletonManager:
    def __init__(self, clz):
        self._clz = clz
        self._instance = None
        
    def get_instance(self):
        if self._instance is None:
            self._instance = self._clz()
            
        return self._instance
    

def singleton(clz):
    singleton_manager = _SingletonManager(clz)
    
    def get_instance():
        return singleton_manager.get_instance()
    
    clz.get_instance = get_instance
    
    return clz


env = _Env()
