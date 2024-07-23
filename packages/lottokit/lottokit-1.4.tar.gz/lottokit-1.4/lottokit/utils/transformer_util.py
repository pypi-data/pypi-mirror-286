#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: transformer_util.py
@DateTime: 2024/7/22 10:26
@SoftWare: PyCharm
"""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from typing import Optional
from .calculate_util import CalculateUtil
from .model_util import ModelUtil


class RandomForestRegressorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model: RandomForestRegressor):
        """
        Initialize the transformer with a RandomForestRegressor model and a StandardScaler for feature scaling.

        Parameters:
        model (RandomForestRegressor): The RandomForestRegressor model to be used for predictions.
        """
        self.calculate_util = CalculateUtil()
        self.model_util = ModelUtil()
        self.model = model
        self.scaler = StandardScaler()

    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> 'RandomForestRegressorTransformer':
        """
        Fit the RandomForest model and the scaler on the training data.

        Parameters:
        X (np.ndarray): Training data features.
        y (Optional[np.ndarray]): Training data labels.

        Returns:
        RandomForestRegressorTransformer: The instance of this transformer.
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform the input data by scaling, making predictions, and calculating per-row statistics.

        Parameters:
        X (np.ndarray): Data to transform.

        Returns:
        np.ndarray: Transformed data including last elements, predictions, standard deviations, and RSI values.
        """
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)

        # Calculate standard deviation and RSI for each row
        sd_per_row = np.array([self.calculate_util.calculate_standard_deviation_welford(row) for row in X])
        rsi_per_row = np.array([self.model_util.relative_strength_index(row, period=len(row) // 2) for row in X])

        # Extract the last element from each row
        last_elements = X[:, -1]

        # Combine all the computed features into a single array
        transformed_data = np.c_[last_elements, predictions, sd_per_row, rsi_per_row]
        return transformed_data
