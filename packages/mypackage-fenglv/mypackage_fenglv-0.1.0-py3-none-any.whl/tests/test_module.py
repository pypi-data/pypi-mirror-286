# tests/test_module.py

import unittest
from mypackage.module import hello_world

class TestModule(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(hello_world(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()