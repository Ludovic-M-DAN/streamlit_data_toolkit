import unittest
import pandas as pd
from src.eda import get_data_info

class TestEDA(unittest.TestCase):
    def test_get_data_info(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['x', 'y', 'z']})
        info = get_data_info(df)
        self.assertEqual(info['dimensions'], (3, 2))
        self.assertEqual(info['column_names'], ['A', 'B'])
        self.assertEqual(info['data_types']['A'], 'int64')
        self.assertEqual(info['missing_values']['A'], 0)
        self.assertEqual(info['missing_values']['B'], 0)

if __name__ == '__main__':
    unittest.main()