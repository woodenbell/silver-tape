from copy import deepcopy, copy
from functools import reduce
from types import FunctionType
from re import compile, Pattern


def _flatten(l):
    return reduce(lambda a, b: a + b, [_flatten(i) if i.__class__ is list else [i] for i in l])


def _list_compare(l1, l2):
    if len(l1) != len(l2):
        return False
    
    for i in range(len(l1)):
        if l1[i].__class__ is list:
            if (l2[i].__class__ is not list) or (not _list_compare(l1[i], l2[i])):
                return False
        elif not l1 == l2:
            return False
    
    return True


def smart(obj):
    if obj.__class__ is list:
        return SmartList(obj)
    if obj.__class__ is dict:
        return SmartDict(obj)
    elif obj.__class__ is SmartList:
        return obj.get_list()
    elif obj.__class__ is SmartDict:
        return obj.get_dict()


class SmartList:
    def __init__(self, val):
        self._val = val
    
    def __mul__(self, other):
        if other.__class__ is int:
            return SmartList(self._val * other)
        elif other.__class__ is FunctionType:
            return SmartList(list(map(other, self._val)))
        
    def __add__(self, other):
        if other.__class__ is list:
            return SmartList(self._val + other)
        else:
            val = deepcopy(self._val)
            val.append(other)
            return SmartList(val)
    
    def __sub__(self, other):
        val = deepcopy(self._val)
        
        if other.__class__ is list:
            for i in other:
                val.remove(i)
            
            return SmartList(val)
        else:
            val.remove(other)
            return SmartList(val)

    def __and__(self, other):
        return SmartList([i for i in self._val if i in other])
    
    def __mod__(self, other):
        if other.__class__ is FunctionType:
            return SmartList(list(filter(other, self._val)))
    
    def __xor__(self, other):
        return SmartList(list(zip(self._val, other)))
    
    def __getitem__(self, item):
        if item.__class__ is slice:
            return SmartList(self._val[item])
        elif item.__class__ is list:
            return SmartList(list(map(lambda x: self._val[x], item)))
        elif item.__class__ is FunctionType:
            return self.find(item)
        else:
            return self._val[item]
    
    def __setitem__(self, key, value):
        self._val.__setitem__(key, value)
    
    def __contains__(self, item):
        return item in self._val
    
    def __delitem__(self, item):
        self._val.__delitem__(item)
        
    def __iter__(self):
        return self._val.__iter__()
    
    def __len__(self):
        return len(self._val)
    
    def __eq__(self, other):
        return _list_compare(self._val, other)
    
    def __ne__(self, other):
        return not _list_compare(self._val, other)
    
    def __lt__(self, other):
        return len(self._val) < len(other)
    
    def __gt__(self, other):
        return len(self._val) > len(other)
    
    def __le__(self, other):
        return len(self._val) <= len(other)
    
    def __ge__(self, other):
        return len(self._val) >= len(other)
    
    def __invert__(self):
        return SmartList(_flatten(self._val))
    
    def __hash__(self):
        return self._val.__hash__()
    
    def __reversed__(self):
        return self._val.__reversed__()
    
    def __repr__(self):
        return self._val.__repr__()
    
    def append(self, obj):
        self._val.append(obj)
        
    def clear(self):
        self._val.clear()
        
    def copy(self):
        return copy(self)
    
    def count(self, value):
        return self._val.count(value)
    
    def extend(self, iterable):
        self._val.extend(iterable)
    
    def index(self, value, start=0, stop=2147483647):
        return self._val.index(value, start=start, stop=stop)
    
    def insert(self, index, obj):
        self._val.insert(index, obj)
        
    def pop(self, index=-1):
        return self._val.pop(index=index)
    
    def remove(self, value):
        self._val.remove(value)
        
    def reverse(self):
        self._val.reverse()
    
    def sort(self, key=None, reverse=False):
        return self._val.sort(key=key, reverse=reverse)
    
    def sum(self):
        return reduce(lambda a, b: a + b, self._val, 0)
    
    def avg(self):
        return self.sum() / len(self._val)
    
    def find(self, cond):
        for i in self._val:
            if cond(i):
                return i
            
        return None
    
    def get_list(self):
        return self._val


def _flatten_dict(d, prefix=None, joiner='-'):
    d2 = {}
    
    for k, v in d.items():
        key = joiner.join([prefix, k]) if prefix else k
        
        if v.__class__ is dict:
            d2 = {**d2, **_flatten_dict(v, prefix=key, joiner=joiner)}
        else:
            d2[key] = v
    return d2


class SmartDict:
    def __init__(self, val):
        self._val = val
    
    def __getitem__(self, key):
        if key.__class__ is list:
            d = {}
            
            for i in key:
                d[i] = self._val[i]
            
            return SmartDict(d)
        else:
            return self._val.__getitem__(key)
    
    def __setitem__(self, key, value):
        self._val.__setitem__(key, value)
        
    def __delitem__(self, key):
        self._val.__delitem__(key)
    
    def __contains__(self, item):
        return item in self._val
        
    def __add__(self, other):
        return SmartDict({**self._val, **other})
    
    def __mod__(self, other):
        patt = None
        
        if other.__class__ is str:
            patt = compile(other)
        elif other.__class__ is Pattern:
            patt = other
        else:
            raise TypeError('SmartDict key filter value must be regex pattern or valid pattern string')
        
        d = {}
        
        for k, v in self._val.items():
            if patt.match(k):
                d[k] = v
        
        return SmartDict(d)
        
    def __invert__(self):
        return self.flatten()
        
    def __repr__(self):
        return self._val.__repr__()
    
    def flatten(self, joiner='-'):
        return SmartDict(_flatten_dict(self._val, joiner=joiner))
    
    def copy(self):
        return copy(self)
    
    def items(self):
        return self._val.items()
    
    def keys(self):
        return self._val.keys()
    
    def values(self):
        return self._val.values()
    
    def get_dict(self):
        return self._val
