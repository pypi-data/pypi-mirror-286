import unittest
import pandas as pd
from DataPrepToolkit.data_cleaning import DataCleaner

class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': [None, None, None, None],
            'C': [1, 2, 3, 4],
            'D': [1, 2, 3, None],
            'E': ['a', 'b', None, 'b']
        })
        self.cleaner = DataCleaner(self.df)

    def test_show_missing_values(self):
        self.cleaner.show_missing_values()

    def test_missing_values_percentage(self):
        self.cleaner.missing_values_percentage()

    def test_remove_missing_values(self):
        cleaned_df = self.cleaner.remove_missing_values(threshold=0.5)
        self.assertListEqual(list(cleaned_df.columns), ['A', 'C', 'D', 'E'])

        cleaned_df_high_threshold = self.cleaner.remove_missing_values(threshold=0.1)
        self.assertListEqual(list(cleaned_df_high_threshold.columns), ['C'])

    def test_fill_missing_values_mean(self):
        filled_df = self.cleaner.fill_missing_values(strategy='mean')
        self.assertAlmostEqual(filled_df['A'].iloc[2], 2.333, places=3)
        self.assertAlmostEqual(filled_df['D'].iloc[3], 2.0, places=1)
        self.assertEqual(filled_df['E'].iloc[2], 'b')

    def test_fill_missing_values_median(self):
        filled_df = self.cleaner.fill_missing_values(strategy='median')
        self.assertAlmostEqual(filled_df['A'].iloc[2], 2.0, places=1)
        self.assertAlmostEqual(filled_df['D'].iloc[3], 2.0, places=1)
        self.assertEqual(filled_df['E'].iloc[2], 'b')

    def test_fill_missing_values_mode(self):
        filled_df = self.cleaner.fill_missing_values(strategy='mode')
        self.assertAlmostEqual(filled_df['A'].iloc[2], 1.0, places=1)
        self.assertAlmostEqual(filled_df['D'].iloc[3], 1.0, places=1)
        self.assertEqual(filled_df['E'].iloc[2], 'b')

    def test_fill_missing_values_invalid_strategy(self):
        with self.assertRaises(ValueError):
            self.cleaner.fill_missing_values(strategy='invalid')

    def test_list_features(self):
        categorical_features, numerical_features = self.cleaner.list_features()
        self.assertListEqual(categorical_features, ['E'])
        self.assertListEqual(numerical_features, ['A', 'C', 'D'])

    def test_summary_statistics(self):
        summary_stats = self.cleaner.summary_statistics()
        self.assertTrue(isinstance(summary_stats, pd.DataFrame))
        self.assertListEqual(list(summary_stats.columns), ['A', 'C', 'D'])

    def test_count_categorical_features(self):
        cat_counts = self.cleaner.count_categorical_features()
        self.assertTrue('E' in cat_counts)
        self.assertEqual(cat_counts['E']['a'], 1)
        self.assertEqual(cat_counts['E']['b'], 2)

if __name__ == '__main__':
    unittest.main()
