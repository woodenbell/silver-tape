from typing import Type


class _Env:
    def __init__(self): ...
    
    def __getattr__(self, item: str) -> str: ...
    
    def __setattr__(self, key: str, value: str): ...
    
    def __delattr__(self, item: str): ...
    

class _SingletonManager:
    def __init__(self, clz: Type): pass
    

def singleton(clz: Type) -> Type: ...

env = None  # type: _Env