import unittest
import pandas as pd
from src.data_loader import load_data, sample_data
import os

class TestDataLoader(unittest.TestCase):
    def test_load_data_csv(self):
        # Crée un fichier CSV temporaire pour tester
        with open("test_sample.csv", "w") as f:
            f.write("col1,col2\n1,2\n3,4")
        data = load_data("test_sample.csv", separator=',')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(data.shape, (2, 2))
        self.assertEqual(list(data.columns), ["col1", "col2"])
        os.remove("test_sample.csv")  # Nettoie après le test

    def test_sample_data_random_total(self):
        df = pd.DataFrame({'A': range(10), 'B': ['x'] * 10})
        sampled = sample_data(df, 'random_total', n=5)
        self.assertEqual(len(sampled), 5)
        self.assertTrue(all(col in df.columns for col in sampled.columns))

    def test_sample_data_first_n(self):
        df = pd.DataFrame({'A': range(10), 'B': ['x'] * 10})
        sampled = sample_data(df, 'first_n', n=3)
        self.assertEqual(len(sampled), 3)
        self.assertEqual(sampled['A'].tolist(), [0, 1, 2])

if __name__ == '__main__':
    unittest.main()