from unittest import TestCase
from silvertape.util import env, singleton


class TestUtil(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_env(self):
        env.TOKEN = 'abx382jxndr'
        
        self.assertEqual(env.TOKEN, 'abx382jxndr')
        
    def test_singleton(self):
        count = {'n': 0}
        
        @singleton
        class A:
            def __init__(self):
                count['n'] += 1
                
        a = A.get_instance()
        b = A.get_instance()
        
        self.assertEqual(count['n'], 1)
