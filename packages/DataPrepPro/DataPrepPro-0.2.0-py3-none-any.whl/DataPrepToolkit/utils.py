"""
utils.py
========

This module contains utility functions for the DataPrepToolkit package.
"""

import pandas as pd
import logging

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    return pd.read_csv(file_path)

def save_data(df: pd.DataFrame, file_path: str):
    """
    Save dataframe to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe to save.
        file_path (str): The path to the CSV file.
    """
    df.to_csv(file_path, index=False)

def setup_logging(log_file: str):
    """
    Set up logging configuration.

    Args:
        log_file (str): The path to the log file.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log(message: str, level: str = 'info'):
    """
    Log a message.

    Args:
        message (str): The message to log.
        level (str): The logging level ('info', 'warning', 'error'). Default is 'info'.
    """
    if level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    else:
        raise ValueError("Logging level not recognized. Use 'info', 'warning', or 'error'.")

def calculate_missing_values_percentage(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the percentage of missing values for each column.

    Args:
        df (pd.DataFrame): The dataframe to analyze.

    Returns:
        pd.Series: A series with the percentage of missing values for each column.
    """
    return (df.isnull().sum() / len(df)) * 100
