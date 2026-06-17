"""
Module for loading data from various sources
"""

import pandas as pd
import os
from pathlib import Path


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load raw data from CSV file
    
    Args:
        filepath (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"Loaded data shape: {df.shape}")
    return df


def load_processed_data(filepath: str) -> pd.DataFrame:
    """
    Load processed data from CSV file
    
    Args:
        filepath (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Loaded processed data
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    return df


def save_data(df: pd.DataFrame, filepath: str) -> None:
    """
    Save data to CSV file
    
    Args:
        df (pd.DataFrame): Data to save
        filepath (str): Output path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Data saved to: {filepath}")
