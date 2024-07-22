"""
feature_engineering.py
======================

This module contains functions for engineering features and visualizing feature distributions.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class FeatureEngineer:
    """Class for feature engineering and visualizing feature distributions."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with the dataframe to be engineered and visualized.

        Args:
            df (pd.DataFrame): The dataframe to engineer and visualize.
        """
        self.df = df

    def plot_feature_distribution(self, columns: list):
        """
        Plot the distribution of specified columns.

        Args:
            columns (list): List of columns to plot.
        """
        for column in columns:
            plt.figure(figsize=(10, 5))
            if self.df[column].dtype == 'object':
                sns.countplot(data=self.df, x=column, palette='viridis')
                plt.title(f'Distribution of {column}')
            else:
                sns.histplot(data=self.df, x=column, kde=True, color='skyblue')
                plt.title(f'Distribution of {column}')
            plt.show()

    def plot_correlation_heatmap(self):
        """
        Plot a heatmap of correlations between numerical features.
        """
        plt.figure(figsize=(12, 6))
        correlation_matrix = self.df.select_dtypes(include=['number']).corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.show()

    def encode_categorical(self, columns: list, drop_first: bool = False) -> pd.DataFrame:
        """
        Encode categorical columns using one-hot encoding.

        Args:
            columns (list): List of columns to encode.
            drop_first (bool): Whether to drop the first category in each encoded column to avoid the dummy variable trap. Default is False.

        Returns:
            pd.DataFrame: The dataframe with encoded columns.
        """
        # Encode the specified columns using one-hot encoding
        self.df = pd.get_dummies(self.df, columns=columns, drop_first=drop_first)
        return self.df

    def normalize_features(self, columns: list) -> pd.DataFrame:
        """
        Normalize specified columns.

        Args:
            columns (list): List of columns to normalize.

        Returns:
            pd.DataFrame: The dataframe with normalized columns.
        """
        self.df[columns] = (self.df[columns] - self.df[columns].mean()) / self.df[columns].std()
        return self.df
