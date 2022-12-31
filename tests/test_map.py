import unittest
from source.environment._map import *

class TestMap(unittest.TestCase):
    
    def test_map_constructor(self):
        _map = map("Test1")
        self.assertEqual(_map.name, "Test2", "Map constructor test passed")
        
        

if __name__ == '__main_test__':
    unittest.main()