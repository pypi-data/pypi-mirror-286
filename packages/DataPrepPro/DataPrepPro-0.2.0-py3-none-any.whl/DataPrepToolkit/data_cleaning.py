import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataCleaner with a dataframe.

        Args:
            df (pd.DataFrame): The dataframe to clean.
        """
        self.df = df

    def show_missing_values(self):
        """
        Visualize missing values in the dataframe.
        """
        plt.figure(figsize=(12, 6))
        sns.heatmap(self.df.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Values Heatmap')
        plt.show()

    def missing_values_percentage(self):
        """
        Plot the percentage of missing values for each column.
        """
        missing_percentage = self.df.isnull().mean() * 100
        missing_percentage = missing_percentage[missing_percentage > 0]
        missing_percentage.sort_values(inplace=True)
        
        missing_percentage.plot.bar()
        plt.ylabel('Percentage of Missing Values')
        plt.title('Missing Values Percentage')
        plt.show()

    def remove_missing_values(self, threshold: float = 0.5) -> pd.DataFrame:
        """
        Remove columns with missing values above a certain threshold.

        Args:
            threshold (float): The threshold for removing columns.

        Returns:
            pd.DataFrame: The dataframe with columns removed.
        """
        self.df = self.df.loc[:, self.df.isnull().mean() < threshold]
        return self.df

    def fill_missing_values(self, strategy: str = 'mean') -> pd.DataFrame:
        """
        Fill missing values in the dataframe.

        Args:
            strategy (str): The strategy to fill missing values ('mean', 'median', 'mode').

        Returns:
            pd.DataFrame: The dataframe with filled values.
        """
        if strategy not in ['mean', 'median', 'mode']:
            raise ValueError("Strategy not recognized. Use 'mean', 'median', 'mode'.")

        # Fill missing values for numerical columns
        numerical_cols = self.df.select_dtypes(include=['number']).columns
        if strategy == 'mean':
            self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].mean())
        elif strategy == 'median':
            self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].median())
        elif strategy == 'mode':
            self.df[numerical_cols] = self.df[numerical_cols].apply(lambda x: x.fillna(x.mode().iloc[0]))

        # Fill missing values for categorical columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        self.df[categorical_cols] = self.df[categorical_cols].apply(lambda x: x.fillna(x.mode().iloc[0]) if not x.mode().empty else x)

        return self.df

    def list_features(self) -> (list, list):
        """
        List categorical and numerical features in the dataframe.

        Returns:
            tuple: A tuple containing a list of categorical features and a list of numerical features.
        """
        categorical_features = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        numerical_features = self.df.select_dtypes(include=['number']).columns.tolist()

        # Exclude columns with all missing values
        categorical_features = [col for col in categorical_features if not self.df[col].isnull().all()]

        return categorical_features, numerical_features

    def summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for numerical features.

        Returns:
            pd.DataFrame: A dataframe containing summary statistics.
        """
        numerical_features = self.df.select_dtypes(include=['number']).columns
        return self.df[numerical_features].describe()

    def count_categorical_features(self) -> dict:
        """
        Count occurrences of each category in categorical features.

        Returns:
            dict: A dictionary with feature names as keys and counts as values.
        """
        categorical_features = self.df.select_dtypes(include=['object', 'category']).columns
        return {col: self.df[col].value_counts().to_dict() for col in categorical_features}
