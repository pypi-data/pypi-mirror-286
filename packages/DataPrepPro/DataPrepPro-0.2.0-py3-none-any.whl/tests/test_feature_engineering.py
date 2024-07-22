import unittest
import pandas as pd
from DataPrepToolkit.feature_engineering import FeatureEngineer

class TestFeatureEngineer(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'A': ['a', 'b', 'a', 'c'],
            'B': [1, 2, 3, 4],
            'C': ['x', 'y', 'x', 'z'],
            'D': [0.1, 0.2, 0.3, 0.4]
        })
        self.engineer = FeatureEngineer(self.df)

    def test_plot_feature_distribution(self):
        self.engineer.plot_feature_distribution(columns=['A', 'B', 'C'])

    def test_plot_correlation_heatmap(self):
        self.engineer.plot_correlation_heatmap()

    def test_encode_categorical(self):
        self.setUp()  # Reset the DataFrame
        encoded_df = self.engineer.encode_categorical(columns=['A', 'C'])
        self.assertListEqual(
            list(encoded_df.columns),
            ['B', 'D', 'A_a', 'A_b', 'A_c', 'C_x', 'C_y', 'C_z']
        )

        self.setUp()  # Reset the DataFrame
        encoded_df_drop_first = self.engineer.encode_categorical(columns=['A', 'C'], drop_first=True)
        self.assertListEqual(
            list(encoded_df_drop_first.columns),
            ['B', 'D', 'A_b', 'A_c', 'C_y', 'C_z']
        )

    def test_normalize_features(self):
        normalized_df = self.engineer.normalize_features(columns=['B', 'D'])
        self.assertAlmostEqual(normalized_df['B'].mean(), 0.0, places=1)
        self.assertAlmostEqual(normalized_df['B'].std(), 1.0, places=1)
        self.assertAlmostEqual(normalized_df['D'].mean(), 0.0, places=1)
        self.assertAlmostEqual(normalized_df['D'].std(), 1.0, places=1)

    def test_normalize_empty_column_list(self):
        normalized_df = self.engineer.normalize_features(columns=[])
        self.assertTrue(normalized_df.equals(self.df))

if __name__ == '__main__':
    unittest.main()
