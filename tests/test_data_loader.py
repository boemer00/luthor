import unittest
from io import BytesIO
from src.data_loader import read_file

class TestReadFile(unittest.TestCase):
    def test_loading(self):
        dummy_file = BytesIO(b"Test content")
        result = read_file(dummy_file, "test.txt")
        self.assertIsNotNone(result)
        self.assertEqual(result, "Test content")

if __name__ == '__main__':
    unittest.main()
