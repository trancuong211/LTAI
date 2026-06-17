"""
Model prediction module
- Make predictions on new data
"""

import pandas as pd
import numpy as np
import joblib


class ModelPredictor:
    """Class for making predictions with trained model"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize ModelPredictor
        
        Args:
            model_path (str): Path to saved model file
        """
        self.model = None
        if model_path:
            self.load_model(model_path)
    
    
    def load_model(self, model_path: str) -> None:
        """
        Load trained model
        
        Args:
            model_path (str): Path to model file
        """
        self.model = joblib.load(model_path)
        print(f"Model loaded from: {model_path}")
    
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions
        
        Args:
            X (pd.DataFrame): Features for prediction
        
        Returns:
            np.ndarray: Predictions
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        predictions = self.model.predict(X)
        return predictions
    
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make probability predictions (for classification models)
        
        Args:
            X (pd.DataFrame): Features for prediction
        
        Returns:
            np.ndarray: Probability predictions
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        if not hasattr(self.model, 'predict_proba'):
            raise ValueError("Model does not support probability prediction")
        
        return self.model.predict_proba(X)
    
    
    def batch_predict(self, X: pd.DataFrame, batch_size: int = 1000) -> np.ndarray:
        """
        Make batch predictions
        
        Args:
            X (pd.DataFrame): Features for prediction
            batch_size (int): Batch size
        
        Returns:
            np.ndarray: Predictions
        """
        predictions = []
        for i in range(0, len(X), batch_size):
            batch = X[i:i+batch_size]
            batch_pred = self.predict(batch)
            predictions.extend(batch_pred)
        
        return np.array(predictions)
