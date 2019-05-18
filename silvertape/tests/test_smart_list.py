from copy import copy, deepcopy
from unittest import TestCase
from silvertape.smart import smart


class TestSmartList(TestCase):
    def setUp(self):
        self.test_list = list(range(1, 21))
        self.smart_list = smart(self.test_list)
    
    def tearDown(self):
        del self.test_list
        del self.smart_list
    
    def test_get_item(self):
        self.assertEqual(self.smart_list[2], 3)
    
    def test_get_slice(self):
        self.assertListEqual(smart(self.smart_list[1:4]), [2, 3, 4])
        
    def test_set_item(self):
        copy_list = deepcopy(self.smart_list)
        copy_list[2] = 9
        
        self.assertEqual(copy_list[2], 9)
    
    def test_find_item(self):
        self.assertEqual(self.smart_list[lambda x: x == 5], 5)
        
    def test_get_multiple(self):
        result = self.smart_list[[2, 4, -1]]
        list_result = smart(result)
        
        self.assertListEqual(list_result, [3, 5, 20])
    
    def test_del_item(self):
        copy_list = deepcopy(self.smart_list)
        del copy_list[4]
        result_list = smart(copy_list)
        
        self.assertFalse(5 in result_list)
    
    def test_del_slice(self):
        copy_list = deepcopy(self.smart_list)
        del copy_list[0:10]
        result_list = smart(copy_list)
        compare_list = list(range(11, 21))
        
        self.assertListEqual(result_list, compare_list)
    
    def test_step(self):
        self.assertListEqual(smart(self.smart_list[::5]), [1, 6, 11, 16])
    
    def test_map(self):
        result = self.smart_list * (lambda x: x * 2)
        
        for i in range(len(result)):
            self.assertEqual(result[i], self.smart_list[i] * 2)
    
    def test_mul(self):
        result = self.smart_list * 2
        
        self.assertListEqual(smart(result), self.test_list * 2)
    
    def test_concat(self):
        result = self.smart_list + [21, 22, 23]
    
        self.assertListEqual(smart(result), self.test_list + [21, 22, 23])
    
    def test_add_item(self):
        normal_list = copy(self.test_list)
        result = self.smart_list + 21
        normal_list.append(21)
    
        self.assertListEqual(smart(result), normal_list)
    
    def test_single_remove(self):
        normal_list = copy(self.test_list)
        result = self.smart_list - 20
        normal_list.remove(20)
    
        self.assertListEqual(smart(result), normal_list)

    def test_multiple_remove(self):
        normal_list = copy(self.test_list)
        result = self.smart_list - [18, 19, 20]
        
        for i in [18, 19, 20]:
            normal_list.remove(i)
    
        self.assertListEqual(smart(result), normal_list)
    
    def test_intersection(self):
        result = self.smart_list & [1, 2, 3, 99]

        self.assertListEqual(smart(result), [1, 2, 3])
        
    def test_filter(self):
        normal_list = copy(self.test_list)
        result = self.smart_list % (lambda x: not x % 2)
        normal_result = list(filter(lambda x: not x % 2, normal_list))
        
        self.assertListEqual(smart(result), normal_result)
    
    def test_zip(self):
        result = self.smart_list ^ self.test_list
        
        for i in result:
            self.assertTrue(i[0] == i[1])
    
    def test_iter(self):
        for i in self.smart_list:
            self.assertTrue(i in self.test_list)
    
    def test_contains(self):
        self.assertTrue(1 in self.smart_list)
        
    def test_len(self):
        self.assertEqual(len(self.smart_list), 20)
    
    def test_equals(self):
        self.assertTrue(self.smart_list == self.test_list)
    
    def test_not_equals(self):
        normal_list = copy(self.test_list)
        normal_list[-1] = 21
        
        self.assertFalse(self.smart_list == normal_list)
    
    def test_comparisons(self):
        normal_list1 = [1, 2, 3]
        normal_list2 = list(range(1, 31))
        copy_list = deepcopy(self.smart_list)
        
        self.assertTrue(self.smart_list > normal_list1)
        self.assertTrue(self.smart_list >= normal_list1)
        self.assertTrue(self.smart_list < normal_list2)
        self.assertTrue(self.smart_list <= normal_list2)
        self.assertTrue(self.smart_list == copy_list)
        self.assertTrue(self.smart_list != normal_list1)
    
    def test_flatten(self):
        example_list = smart([1, [2, 3, [4]], [5, 6], 7, [8, [[9, [[10]]]]]])
        comparison_list = list(range(1, 11))
        result = smart(~example_list)
        
        self.assertListEqual(result, comparison_list)
        
    def test_reversed(self):
        reversed_list = list(reversed(self.smart_list))
        comparison_list = list(reversed(self.test_list))
        
        self.assertListEqual(reversed_list, comparison_list)
    
    def test_repr(self):
        self.assertEqual(str(self.smart_list), str(self.test_list))
    
    def test_append(self):
        example_list = smart([1, 2, 3])
        example_list.append(4)
        
        self.assertEqual(example_list[3], 4)
    
    def test_sum(self):
        self.assertEqual(self.smart_list.sum(), 210)
    
    def test_avg(self):
        self.assertEqual(self.smart_list.avg(), 10.5)
    
    def test_find(self):
        self.assertEqual(self.smart_list.find(lambda x: x > 5), 6)
        
    def test_copy(self):
        copy_list = self.smart_list.copy()
        
        self.assertListEqual(smart(self.smart_list), smart(copy_list))
    
    def test_convert_normal(self):
        self.assertListEqual(smart(self.smart_list), self.test_list)
