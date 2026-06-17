"""
Data preprocessing module
- Handle missing values
- Remove outliers
- Encoding categorical variables
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """
    Handle missing values in dataset
    
    Args:
        df (pd.DataFrame): Input dataframe
        strategy (str): Strategy to handle missing values
                       ('mean', 'median', 'drop', 'forward_fill')
    
    Returns:
        pd.DataFrame: Dataframe with missing values handled
    """
    df_copy = df.copy()
    
    if strategy == 'drop':
        df_copy = df_copy.dropna()
    elif strategy == 'mean':
        numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
    elif strategy == 'median':
        numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())
    elif strategy == 'forward_fill':
        df_copy = df_copy.fillna(method='ffill')
    
    print(f"Missing values handled using '{strategy}' strategy")
    return df_copy


def remove_outliers(df: pd.DataFrame, columns: list, threshold: float = 3.0) -> pd.DataFrame:
    """
    Remove outliers using Z-score method
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): Columns to check for outliers
        threshold (float): Z-score threshold
    
    Returns:
        pd.DataFrame: Dataframe without outliers
    """
    df_copy = df.copy()
    
    for col in columns:
        if col in df_copy.columns:
            z_scores = np.abs((df_copy[col] - df_copy[col].mean()) / df_copy[col].std())
            df_copy = df_copy[z_scores < threshold]
    
    print(f"Outliers removed. Shape after removal: {df_copy.shape}")
    return df_copy


def encode_categorical(df: pd.DataFrame, categorical_cols: list, method: str = 'label') -> pd.DataFrame:
    """
    Encode categorical variables
    
    Args:
        df (pd.DataFrame): Input dataframe
        categorical_cols (list): List of categorical columns
        method (str): Encoding method ('label' or 'onehot')
    
    Returns:
        pd.DataFrame: Dataframe with encoded categorical variables
    """
    df_copy = df.copy()
    
    if method == 'label':
        le = LabelEncoder()
        for col in categorical_cols:
            if col in df_copy.columns:
                df_copy[col] = le.fit_transform(df_copy[col].astype(str))
    
    elif method == 'onehot':
        df_copy = pd.get_dummies(df_copy, columns=categorical_cols, drop_first=True)
    
    print(f"Categorical encoding completed using '{method}' method")
    return df_copy


def scale_features(df: pd.DataFrame, columns: list = None, scaler_type: str = 'standard') -> tuple:
    """
    Scale numerical features
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): Columns to scale. If None, scale all numeric columns
        scaler_type (str): Type of scaler ('standard' or 'minmax')
    
    Returns:
        tuple: (scaled dataframe, scaler object)
    """
    df_copy = df.copy()
    
    if columns is None:
        columns = df_copy.select_dtypes(include=[np.number]).columns.tolist()
    
    if scaler_type == 'standard':
        scaler = StandardScaler()
    else:
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
    
    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    print(f"Features scaled using '{scaler_type}' scaler")
    
    return df_copy, scaler
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full preprocessing pipeline: handle missing values and encode categorical variables
    
    Args:
        df (pd.DataFrame): Raw input dataframe
    
    Returns:
        pd.DataFrame: Preprocessed dataframe
    """
    # Xử lý missing values
    df = handle_missing_values(df, strategy='mean')
    
    # Tự động tìm các cột dạng chữ (categorical) để encode
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        df = encode_categorical(df, categorical_cols, method='label')
    
    return df