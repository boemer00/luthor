import unittest
from src.data_loader import read_file

class TestReadFile(unittest.TestCase):
    def test_loading(self):
        loader = read_file()
        self.assertIsNotNone(loader)

if __name__ == '__main__':
    unittest.main()
