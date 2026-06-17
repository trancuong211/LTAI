"""
Model training module
- Train various ML models
- Hyperparameter tuning
- Model selection
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV


class ModelTrainer:
    """Class for training and managing models"""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize ModelTrainer
        
        Args:
            random_state (int): Random state for reproducibility
        """
        self.random_state = random_state
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
    
    
    def prepare_data(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> None:
        """
        Prepare train-test split
        
        Args:
            X (pd.DataFrame): Features
            y (pd.Series): Target variable
            test_size (float): Test set size ratio
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        self.feature_names = X.columns.tolist()
        print(f"Data prepared. Train shape: {self.X_train.shape}, Test shape: {self.X_test.shape}")
    
    
    def train_linear_regression(self) -> None:
        """Train Linear Regression model"""
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        print("Linear Regression model trained")
    
    
    def train_ridge_regression(self, alpha: float = 1.0) -> None:
        """Train Ridge Regression model"""
        self.model = Ridge(alpha=alpha, random_state=self.random_state)
        self.model.fit(self.X_train, self.y_train)
        print(f"Ridge Regression model trained (alpha={alpha})")
    
    
    def train_lasso_regression(self, alpha: float = 1.0) -> None:
        """Train Lasso Regression model"""
        self.model = Lasso(alpha=alpha, random_state=self.random_state)
        self.model.fit(self.X_train, self.y_train)
        print(f"Lasso Regression model trained (alpha={alpha})")
    
    
    def train_random_forest(self, n_estimators: int = 100, max_depth: int = None) -> None:
        """Train Random Forest model"""
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=self.random_state,
            n_jobs=-1
        )
        self.model.fit(self.X_train, self.y_train)
        print(f"Random Forest model trained (n_estimators={n_estimators})")
    
    
    def train_gradient_boosting(self, n_estimators: int = 100, learning_rate: float = 0.1) -> None:
        """Train Gradient Boosting model"""
        self.model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)
        print(f"Gradient Boosting model trained (n_estimators={n_estimators})")
    
    
    def train_svr(self, kernel: str = 'rbf', C: float = 100) -> None:
        """Train Support Vector Regression model"""
        self.model = SVR(kernel=kernel, C=C)
        self.model.fit(self.X_train, self.y_train)
        print(f"SVM model trained (kernel={kernel})")
    
    
    def cross_validate(self, cv: int = 5) -> dict:
        """
        Perform cross-validation
        
        Args:
            cv (int): Number of folds
        
        Returns:
            dict: Cross-validation scores
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        scores = cross_val_score(self.model, self.X_train, self.y_train, 
                                cv=cv, scoring='r2')
        print(f"Cross-validation R² scores: {scores}")
        return {'scores': scores, 'mean': scores.mean(), 'std': scores.std()}
    
    
    def save_model(self, filepath: str) -> None:
        """
        Save model to file
        
        Args:
            filepath (str): Path to save model
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"Model saved to: {filepath}")
    
    
    def load_model(self, filepath: str) -> None:
        """
        Load model from file
        
        Args:
            filepath (str): Path to load model from
        """
        self.model = joblib.load(filepath)
        print(f"Model loaded from: {filepath}")

def train_model(df: pd.DataFrame, target_column: str = 'price', model_type: str = 'random_forest'):
    """
    Train a model using ModelTrainer pipeline
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe (features + target)
        target_column (str): Name of the target column (giá nhà)
        model_type (str): 'linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting', or 'svr'
    
    Returns:
        tuple: (trained model, X_test, y_test)
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    trainer = ModelTrainer(random_state=42)
    trainer.prepare_data(X, y)
    
    if model_type == 'linear':
        trainer.train_linear_regression()
    elif model_type == 'ridge':
        trainer.train_ridge_regression()
    elif model_type == 'lasso':
        trainer.train_lasso_regression()
    elif model_type == 'random_forest':
        trainer.train_random_forest()
    elif model_type == 'gradient_boosting':
        trainer.train_gradient_boosting()
    elif model_type == 'svr':
        trainer.train_svr()
    
    return trainer.model, trainer.X_test, trainer.y_test