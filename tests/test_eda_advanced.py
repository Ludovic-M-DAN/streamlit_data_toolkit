import unittest
import pandas as pd
from src.eda_advanced import descriptive_stats, plot_distribution, plot_correlation, plot_missing_values, plot_boxplot

class TestEDAAdvanced(unittest.TestCase):
    def test_descriptive_stats(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
        stats = descriptive_stats(df)
        self.assertEqual(stats.loc['mean', 'A'], 3.0)
        self.assertEqual(stats.loc['min', 'A'], 1.0)
        self.assertEqual(stats.loc['max', 'A'], 5.0)

    def test_plot_distribution(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
        fig = plot_distribution(df, 'A')
        self.assertIsNotNone(fig)

    def test_plot_correlation(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        fig = plot_correlation(df)
        self.assertIsNotNone(fig)

    def test_plot_missing_values(self):
        df = pd.DataFrame({'A': [1, None, 3], 'B': [4, 5, 6]})
        fig = plot_missing_values(df)
        self.assertIsNotNone(fig)

    def test_plot_boxplot(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
        fig = plot_boxplot(df, 'A')
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()