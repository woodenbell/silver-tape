from typing import Callable, Any, Union, Dict


class _NFunc:
    def __init__(self, n: int):
        self._n = None  # type: int
        self._called = None  # type: int
        ...
    
    def try_call(self) -> bool: ...


class Pipe:
    class Value:
        pass
    
    def __init__(self, val: Any):
        self._val = None  # type: Any
    
    def __or__(self, other: Union[Callable, Any]) -> Union[Pipe, Any]: ...


def compose(*fl: Callable) -> Callable: ...


def _n_calls(f: Callable, obj: _NFunc): ...


def once(f: Callable) -> Callable: ...
    

def only(n: int) -> Callable[[Callable], Callable]: ...


def only_if(should: bool) -> Callable[[Callable], Callable]: ...

class FunctionCollector:
    def __init__(self, **kwargs: Callable):
        self._handlers = None  # type: Dict[str, Callable]
        self._collected = None  # type: Dict[str, Dict[str, (Callable, Any)]]
        ...
    
    def handler(self, name: str) -> Callable: ...
    
    def get_collected(self) -> Dict[str, Dict[str, (Callable, Any)]]: ...