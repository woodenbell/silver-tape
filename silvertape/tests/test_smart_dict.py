from copy import deepcopy
from unittest import TestCase
from silvertape.smart import smart
from re import compile


class TestSmartDict(TestCase):
    def setUp(self):
        self.test_dict = {'a': 1, 'b': 2, 'c': 3}
        self.smart_dict = smart(self.test_dict)
    
    def tearDown(self):
        del self.test_dict
        del self.smart_dict
        
    def test_get_item(self):
        self.assertEqual(self.smart_dict['a'], 1)
        
    def test_get_multiple(self):
        filtered_dict = self.smart_dict[['a', 'b']]
        
        self.assertDictEqual(smart(filtered_dict), {'a': 1, 'b': 2})
        
    def test_set_item(self):
        copy_dict = deepcopy(self.smart_dict)
        copy_dict['b'] = 99
        
        self.assertEqual(copy_dict['b'], 99)
        
    def test_del_item(self):
        copy_dict = deepcopy(self.smart_dict)
        del copy_dict['b']
        
        self.assertFalse('b' in copy_dict)
        
    def test_contains(self):
        self.assertTrue('a' in self.smart_dict)
        
    def test_add(self):
        result = self.smart_dict + {'d': 4}
        
        self.assertDictEqual(smart(result), {'a': 1, 'b': 2, 'c': 3, 'd': 4})
    
    def test_mod(self):
        other_dict = smart({'t1': 1, 'ta': 2, 't32': 3, 'j3': 4})
        result1 = other_dict % '^t[0-9]+$'
        result2 = other_dict % compile('^t[0-9]+$')
        
        self.assertDictEqual(smart(result1), {'t1': 1, 't32': 3})
        self.assertDictEqual(smart(result2), {'t1': 1, 't32': 3})
        
    def test_invert(self):
        other_dict = smart({'a': 1, 'b': {'c': 2}})
        flattened = ~other_dict
        
        self.assertDictEqual(smart(flattened), {'a': 1, 'b-c': 2})

    def test_flatten(self):
        other_dict = smart({'a': 1, 'b': {'c': 2}})
        flattened = ~other_dict
    
        self.assertDictEqual(smart(flattened), {'a': 1, 'b-c': 2})
        
    def test_copy(self):
        copy_dict = self.smart_dict.copy()
        
        self.assertDictEqual(smart(self.smart_dict), smart(copy_dict))
        
    def test_items(self):
        self.assertListEqual(list(self.smart_dict.items()), list(self.test_dict.items()))
    
    def test_keys(self):
        self.assertListEqual(list(self.smart_dict.keys()), list(self.test_dict.keys()))
        
    def test_values(self):
        self.assertListEqual(list(self.smart_dict.values()), list(self.test_dict.values()))
        
    def test_convert_normal(self):
        self.assertDictEqual(smart(self.smart_dict), self.test_dict)
