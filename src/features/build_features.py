"""
Feature engineering module
- Create new features from existing ones
- Feature selection
- Feature transformation
"""

import pandas as pd
import numpy as np


def create_polynomial_features(df: pd.DataFrame, columns: list, degree: int = 2) -> pd.DataFrame:
    """
    Create polynomial features
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): Columns to create polynomial features from
        degree (int): Degree of polynomial
    
    Returns:
        pd.DataFrame: Dataframe with polynomial features
    """
    df_copy = df.copy()
    
    for col in columns:
        if col in df_copy.columns:
            for d in range(2, degree + 1):
                df_copy[f'{col}_pow{d}'] = df_copy[col] ** d
    
    print(f"Polynomial features created (degree={degree})")
    return df_copy


def create_interaction_features(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    """
    Create interaction features between two columns
    
    Args:
        df (pd.DataFrame): Input dataframe
        col1 (str): First column
        col2 (str): Second column
    
    Returns:
        pd.DataFrame: Dataframe with interaction feature
    """
    df_copy = df.copy()
    
    if col1 in df_copy.columns and col2 in df_copy.columns:
        df_copy[f'{col1}_x_{col2}'] = df_copy[col1] * df_copy[col2]
    
    return df_copy


def create_log_features(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Create logarithmic features
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): Columns to create log features from
    
    Returns:
        pd.DataFrame: Dataframe with log features
    """
    df_copy = df.copy()
    
    for col in columns:
        if col in df_copy.columns and (df_copy[col] > 0).all():
            df_copy[f'{col}_log'] = np.log(df_copy[col])
    
    print(f"Log features created")
    return df_copy


def create_binning_features(df: pd.DataFrame, column: str, bins: int = 5) -> pd.DataFrame:
    """
    Create binning features
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column to bin
        bins (int): Number of bins
    
    Returns:
        pd.DataFrame: Dataframe with binned feature
    """
    df_copy = df.copy()
    
    if column in df_copy.columns:
        df_copy[f'{column}_binned'] = pd.cut(df_copy[column], bins=bins, labels=False)
    
    return df_copy


def select_features(df: pd.DataFrame, target: str, method: str = 'correlation', k: int = 10) -> list:
    """
    Select most important features
    
    Args:
        df (pd.DataFrame): Input dataframe with target column
        target (str): Target column name
        method (str): Selection method ('correlation', 'mutual_info')
        k (int): Number of features to select
    
    Returns:
        list: Selected feature names
    """
    if method == 'correlation':
        correlations = df.corr()[target].abs().sort_values(ascending=False)
        selected_features = correlations[1:k+1].index.tolist()
    
    elif method == 'mutual_info':
        from sklearn.feature_selection import mutual_info_regression
        X = df.drop(columns=[target])
        y = df[target]
        mi_scores = mutual_info_regression(X, y, random_state=42)
        mi_scores = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
        selected_features = mi_scores[:k].index.tolist()
    
    print(f"Selected {len(selected_features)} features using '{method}' method")
    return selected_features
def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build engineered features tailored to the HCMC housing dataset
    (area, bedrooms, bathrooms, age, district, house_type, legal_status, price)

    Args:
        df (pd.DataFrame): Input dataframe (after preprocessing)

    Returns:
        pd.DataFrame: Dataframe with engineered features
    """
    df = df.copy()

    # Tổng số phòng (phòng ngủ + phòng tắm) — nhà nhiều phòng thường có giá cao hơn
    if 'bedrooms' in df.columns and 'bathrooms' in df.columns:
        df['total_rooms'] = df['bedrooms'] + df['bathrooms']

    # Diện tích trung bình mỗi phòng ngủ
    if 'area' in df.columns and 'bedrooms' in df.columns:
        df['area_per_bedroom'] = df['area'] / df['bedrooms'].replace(0, 1)

    # Phân nhóm tuổi nhà: 0 = Mới (<=5 năm), 1 = Trung bình (6-15 năm), 2 = Cũ (>15 năm)
    # Dùng labels=False để giữ kiểu số, tránh lỗi khi train model (vì bước này
    # chạy SAU preprocess_data, nên cột string mới sẽ không được encode lại)
    if 'age' in df.columns:
        df['age_group'] = pd.cut(df['age'], bins=[-1, 5, 15, 200], labels=False)

    return df