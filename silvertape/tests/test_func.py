from unittest import TestCase
from silvertape.func import compose, once, only, Pipe, FunctionCollector


class TestFunc(TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_compose(self):
        def a(x):
            return x + 5
    
        def b(x):
            return x * 2
    
        def c(x):
            return x - 8
        
        d = compose(a, b, c)
        
        result = d(5)
        
        self.assertEqual(result, 12)
    
    def test_once(self):
        
        @once
        def incr_count(obj):
            obj['count'] += 1
        
        o = {'count': 0}
        
        for i in range(5):
            incr_count(o)
        
        self.assertEqual(o['count'], 1)
    
    def test_only(self):
        
        @only(4)
        def incr_count(obj):
            obj['count'] += 1
        
        o = {'count': 0}
        
        for i in range(10):
            incr_count(o)
        
        self.assertEqual(o['count'], 4)
    
    def test_pipe(self):
        def a(x):
            return x + 5
        
        def b(x):
            return x * 2
        
        def c(x):
            return x - 8
        
        result = Pipe(5) | a | b | c | Pipe.Value
        
        self.assertEqual(result, 12)
    
    def test_func_collector(self):
        collector = FunctionCollector(get=lambda url: url, post=lambda s, typ: (s, typ))
        get = collector.handler('get')
        post = collector.handler('post')
        
        @get('http://server.com')
        def home(args):
            del args
        
        @get('http://server.com/about')
        def about():
            pass
        
        @post('http://server.com/register', 'urlencoded')
        def register(form):
            del form
        
        collected = collector.get_collected()
        self.assertTrue('home' in collected['get'])
        self.assertEqual(collected['get']['home'][1], 'http://server.com')
        self.assertTrue('about' in collected['get'])
        self.assertEqual(collected['get']['about'][1], 'http://server.com/about')
        self.assertTrue('register' in collected['post'])
        self.assertTrue(collected['post']['register'][1], ('http://server.com/register', 'urlencoded'))
