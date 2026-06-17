"""
Model evaluation module
- Calculate performance metrics
- Generate evaluation reports
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error
)


class ModelEvaluator:
    """Class for evaluating model performance"""
    
    @staticmethod
    def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Root Mean Squared Error
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
        
        Returns:
            float: RMSE value
        """
        return np.sqrt(mean_squared_error(y_true, y_pred))
    
    
    @staticmethod
    def calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Error
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
        
        Returns:
            float: MAE value
        """
        return mean_absolute_error(y_true, y_pred)
    
    
    @staticmethod
    def calculate_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate R² Score
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
        
        Returns:
            float: R² value
        """
        return r2_score(y_true, y_pred)
    
    
    @staticmethod
    def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Percentage Error
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
        
        Returns:
            float: MAPE value
        """
        return mean_absolute_percentage_error(y_true, y_pred)
    
    
    @staticmethod
    def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        """
        Calculate all evaluation metrics
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
        
        Returns:
            dict: Dictionary with all metrics
        """
        metrics = {
            'RMSE': ModelEvaluator.calculate_rmse(y_true, y_pred),
            'MAE': ModelEvaluator.calculate_mae(y_true, y_pred),
            'R2': ModelEvaluator.calculate_r2(y_true, y_pred),
            'MAPE': ModelEvaluator.calculate_mape(y_true, y_pred)
        }
        return metrics
    
    
    @staticmethod
    def print_evaluation_report(y_true: np.ndarray, y_pred: np.ndarray, 
                               model_name: str = "Model") -> None:
        """
        Print evaluation report
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            model_name (str): Model name for report
        """
        metrics = ModelEvaluator.evaluate_model(y_true, y_pred)
        
        print("\n" + "="*50)
        print(f"Evaluation Report: {model_name}")
        print("="*50)
        print(f"RMSE (Root Mean Squared Error): {metrics['RMSE']:.4f}")
        print(f"MAE (Mean Absolute Error):      {metrics['MAE']:.4f}")
        print(f"R² Score:                       {metrics['R2']:.4f}")
        print(f"MAPE (Mean Absolute %Error):    {metrics['MAPE']:.4f}")
        print("="*50 + "\n")
        
        return metrics

def evaluate_model(model, X_test, y_test, model_name: str = "Model") -> dict:
    """
    Evaluate a trained model on test data
    
    Args:
        model: Trained model with .predict() method
        X_test: Test features
        y_test: True target values for test set
        model_name (str): Name to display in report
    
    Returns:
        dict: Evaluation metrics (RMSE, MAE, R2, MAPE)
    """
    y_pred = model.predict(X_test)
    metrics = ModelEvaluator.print_evaluation_report(y_test, y_pred, model_name)
    return metrics