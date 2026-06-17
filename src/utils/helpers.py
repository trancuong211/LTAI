"""
Helper functions for common tasks
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path


def load_config(config_path: str) -> dict:
    """
    Load configuration from YAML file
    
    Args:
        config_path (str): Path to config file
    
    Returns:
        dict: Configuration dictionary
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def save_config(config: dict, config_path: str) -> None:
    """
    Save configuration to YAML file
    
    Args:
        config (dict): Configuration dictionary
        config_path (str): Path to save config
    """
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True)


def print_data_info(df: pd.DataFrame) -> None:
    """
    Print information about dataset
    
    Args:
        df (pd.DataFrame): Input dataframe
    """
    print("\n" + "="*50)
    print("Dataset Information")
    print("="*50)
    print(f"Shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")
    print("="*50 + "\n")


def get_numeric_columns(df: pd.DataFrame) -> list:
    """
    Get numeric columns from dataframe
    
    Args:
        df (pd.DataFrame): Input dataframe
    
    Returns:
        list: List of numeric column names
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list:
    """
    Get categorical columns from dataframe
    
    Args:
        df (pd.DataFrame): Input dataframe
    
    Returns:
        list: List of categorical column names
    """
    return df.select_dtypes(include=['object']).columns.tolist()
