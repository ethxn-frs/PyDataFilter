import unittest
from src.data_loader import load_csv, load_json, load_yaml, load_xml

class TestDataLoader(unittest.TestCase):
    def test_load_csv(self):
        data = load_csv('data/sample_data.csv')
        self.assertIsInstance(data, list)

    def test_load_json(self):
        data = load_json('data/sample_data.json')
        self.assertIsInstance(data, list)

    def test_load_yaml(self):
        data = load_yaml('data/sample_data.yaml')
        self.assertIsInstance(data, list)

    def test_load_xml(self):
        data = load_xml('data/sample_data.xml')
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
