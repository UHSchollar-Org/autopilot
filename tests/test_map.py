import unittest
from source.environment._map import *

class TestMap(unittest.TestCase):
    
    def test_map_constructor(self):
        _map = map("Test1")
        self.assertEqual(_map.name, "Test1")