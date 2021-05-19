import src
import unittest

class TestInit(unittest.TestCase):
    def setUp(self):
        self.hello_message = "Hello, Playground"
    
    def test_prints_hello_playground(self):
        output = src.hello()
        assert(output == self.hello_message)
    def test_print_out_string(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()