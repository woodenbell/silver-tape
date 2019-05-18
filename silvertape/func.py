from functools import reduce


class _NFunc:
    def __init__(self, n):
        self._n = n
        self._called = 0
    
    def try_call(self):
        if self._called < self._n:
            self._called += 1
            return True
        else:
            return False


class Pipe:
    class Value:
        pass
    
    def __init__(self, val):
        self._val = val
    
    def __or__(self, other):
        if other == Pipe.Value:
            return self._val
        elif '__call__' in other.__class__.__dict__:
            return Pipe(other(self._val))


def compose(*fl):
    return reduce(lambda f, c: lambda *a, **kw: f(c(*a, **kw)), fl[::-1], lambda x: x)


def _n_calls(f, obj):
    def wrapper(*args, **kwargs):
        if obj.try_call():
            return f(*args, **kwargs)
        
    return wrapper


def once(f):
    return _n_calls(f, _NFunc(1))


def only(n):
    return lambda f: _n_calls(f, _NFunc(n))


def only_if(should):
    def outer_wrapper(f):
        def inner_wrapper(*args, **kwargs):
            if should:
                return f(*args, **kwargs)
            else:
                return
        return inner_wrapper
    return outer_wrapper


class FunctionCollector:
    def __init__(self, **kwargs):
        self._handlers = kwargs
        self._collected = {i: {} for i in kwargs}
    
    def handler(self, name):
        def outer_wrapper(*args, **kwargs):
            def inner_wrapper(f):
                self._collected[name][f.__name__] = (f, self._handlers[name](*args, **kwargs))
                return f
            return inner_wrapper
        return outer_wrapper
    
    def get_collected(self):
        return self._collected