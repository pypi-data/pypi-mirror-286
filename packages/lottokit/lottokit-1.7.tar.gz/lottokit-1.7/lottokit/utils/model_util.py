#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: model_util.py
@DateTime: 2024/7/22 10:06
@SoftWare: PyCharm
"""
import math

import numpy as np
import pandas as pd
from pmdarima import auto_arima
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import RandomizedSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Optional, Dict
from .calculate_util import CalculateUtil


class CustomTransformer(BaseEstimator, TransformerMixin):
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

    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> 'CustomTransformer':
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


class ModelUtil:
    @staticmethod
    def exponential_moving_average_next_value(
            numeric_sequence: List[int],
            span: int = 5,
            enable_rolling_difference: bool = False
    ) -> int:
        """
        Calculate the Exponential Moving Average (EMA) and use rolling difference to predict the next value of a sequence.

        EMA is a type of moving average that places a greater weight and significance
        on the most recent data points. It's more responsive to new information compared
        to a simple moving average (SMA).

        :param numeric_sequence: A list or sequence of numbers for which the EMA is to be calculated.
        :param span: The number of periods over which to calculate the EMA. Default is 5.
        :param enable_rolling_difference: weather to enable rolling. default is False
        :return: Predicted next value of the sequence based on EMA and rolling difference.
        :raises ValueError: If the input list is empty or contains non-numeric values.
        """
        if not numeric_sequence:
            raise ValueError("The numeric sequence cannot be empty.")
        if not all(isinstance(x, (int, float)) for x in numeric_sequence):
            raise ValueError("All elements in the numeric sequence must be numbers.")

        # Convert the numeric sequence into a pandas Series object
        series = pd.Series(numeric_sequence)

        # Calculate the EMA using pandas' ewm method
        # Adjust 'min_periods' to handle shorter sequences gracefully
        ema = series.ewm(span=span, min_periods=min(span, len(numeric_sequence)), adjust=False).mean()

        # Calculate rolling difference
        rolling_difference = series.diff()

        # Predict the next value by extrapolating the last rolling difference and the last EMA value
        if len(rolling_difference) > 1 and enable_rolling_difference is True:
            predicted_next_value = ema.iloc[-1] + rolling_difference.iloc[-1]
        else:
            # If there's no enough data to calculate difference, use the last EMA as the prediction
            predicted_next_value = ema.iloc[-1]

        rsi = ModelUtil.relative_strength_index(numeric_sequence, period=len(numeric_sequence))
        # Return the predicted next value rounded to the nearest integer
        if rsi <= 50:
            return math.ceil(predicted_next_value)
        # elif rsi in range(50, 70):
        #     return CalculateUtil.real_round(predicted_next_value)
        else:
            return math.floor(predicted_next_value)

    @staticmethod
    def linear_regression_next_value(numeric_sequence: List[int]) -> int:
        """
        Predicts the next value in a sequence using linear regression.

        Linear regression involves fitting a line to the data points in such a way
        that the distance between the data points and the line is minimized. This function
        uses the method to predict the next value in a given sequence of numbers by fitting
        a model to the sequence and examining the slope of the line.

        :param numeric_sequence: A list or sequence of numbers to model.
        :return: The predicted next value in the sequence as an integer.
        :raises ValueError: If the input sequence is empty or too short for regression analysis.
        """
        if not numeric_sequence:
            raise ValueError("The numeric sequence cannot be empty.")
        if len(numeric_sequence) < 2:
            raise ValueError("The numeric sequence must contain at least two elements for linear regression.")

        # Convert the numeric sequence into a numpy array and reshape for sklearn
        data = np.array(numeric_sequence).reshape(-1, 1)

        # Create an array representing time or the independent variable, reshaped as a column
        index = np.array(range(len(data))).reshape(-1, 1)

        # Create a LinearRegression model and fit it to the data
        model = LinearRegression()
        model.fit(index, data)

        # Predict the next value in the sequence using the fitted model
        prediction = model.predict([[len(data)]])[0][0]

        # Return the predicted value as an integer
        return CalculateUtil.real_round(prediction)

    @staticmethod
    def multivariate_polynomial_regression_next_value(
            numeric_sequence: List[int],
            rolling_size: int = 3,
            degrees: int = 3,
    ) -> float:
        """
        Predicts the next value in a numeric sequence using multivariate polynomial regression.

        This method applies a polynomial regression model to a numeric sequence to predict the next value.
        It utilizes a rolling window approach to create datasets, scales the features, and fits a polynomial
        regression model to make the prediction.

        Args:
            numeric_sequence (List[int]): The list of integers representing the sequence.
            rolling_size (int): The number of elements in each rolling window.
            degrees (int): The degree of the polynomial regression. Defaults to 3.

        Returns:
            float: The predicted next value in the sequence.

        Raises:
            ValueError: If the rolling_size is larger than the size of numeric_sequence.
        """
        if rolling_size > len(numeric_sequence):
            raise ValueError("rolling_size cannot be larger than the size of numeric_sequence")

        # Generate datasets with the specified rolling size
        train_x, train_y = CalculateUtil.generate_datasets_with_rolling_size(
            data=numeric_sequence, rolling_size=rolling_size
        )

        # Preparing input data for model training
        input_x = np.array(train_x)
        output_y = np.array(train_y)

        # Scaling the features
        scaler = StandardScaler()
        input_x_scaled = scaler.fit_transform(input_x)

        # Creating and training the polynomial regression model
        model = make_pipeline(PolynomialFeatures(degrees), LinearRegression())
        model.fit(input_x_scaled, output_y)

        # Preparing the last rolling window of data for prediction
        test_x = np.array([numeric_sequence[-rolling_size:]])
        test_x_scaled = scaler.transform(test_x)

        # Predicting the next value
        pred_y = model.predict(test_x_scaled)
        return pred_y[0]

    @staticmethod
    def harmonic_regression_next_value(numeric_sequence: List[int], frequency: float = 1.0) -> int:
        """
        Predicts the next value in a sequence using harmonic regression.

        Harmonic regression involves fitting a model with sine and cosine components to capture
        periodic patterns in the data. This function predicts the next value in a given sequence
        of numbers by fitting a harmonic model to the sequence.

        :param numeric_sequence: A list or sequence of numbers to model.
        :param frequency: The frequency of the periodic component to model.
        :return: The predicted next value in the sequence as an integer.
        """
        # Create feature matrix X and target vector y
        X = np.array(numeric_sequence[:-1]).reshape(-1, 1)  # All elements except the last one
        y = np.array(numeric_sequence[1:])  # All elements except the first one

        # Generate sine and cosine features based on X and given frequency
        sine_feature = np.sin(2 * np.pi * frequency * X)
        cosine_feature = np.cos(2 * np.pi * frequency * X)

        # Combine original features with sine and cosine features into a single feature matrix
        features = np.hstack((X, sine_feature, cosine_feature))

        # Create a LinearRegression model and fit it to the data with harmonic features
        model = LinearRegression()
        model.fit(features, y)

        # Predict the next value in the sequence using the last element of numeric_sequence as input
        next_value = np.array([[numeric_sequence[-1]]])
        next_sine_feature = np.sin(2 * np.pi * frequency * next_value)
        next_cosine_feature = np.cos(2 * np.pi * frequency * next_value)
        next_features = np.hstack((next_value, next_sine_feature, next_cosine_feature))

        next_value = model.predict(next_features)[0]

        # Return the predicted value as an integer
        return CalculateUtil.real_round(next_value)

    @staticmethod
    def random_forest_regressor_transformer(
            numeric_sequence: List[int],
            rolling_size: int,
            warm_start: bool = False,
            random_state: int = 12,
            param_distributions: Optional[Dict] = None,
            param_overrides: Optional[Dict] = None
    ) -> float:
        train_x, train_y = CalculateUtil.generate_datasets_with_rolling_size(
            data=numeric_sequence, rolling_size=rolling_size
        )

        # Convert lists to numpy arrays for compatibility with scikit-learn
        input_x = np.array(train_x)
        output_y = np.array(train_y)

        # Scale the features to normalize data
        scaler = StandardScaler()
        input_x_scaled = scaler.fit_transform(input_x)

        # Initialize and train the Random Forest Regressor
        model = RandomForestRegressor(warm_start=warm_start, random_state=random_state)
        if param_distributions:
            param_overrides = param_overrides or {}
            random_search = RandomizedSearchCV(estimator=model, param_distributions=param_distributions,
                                               **param_overrides)
            random_search.fit(input_x_scaled, output_y)
            model = RandomForestRegressor(warm_start=warm_start, random_state=random_state,
                                          **random_search.best_params_)

        model_pipline = Pipeline([
            ('prediction_transformer', CustomTransformer(model)),
            ('prediction_transformer_two', RandomForestRegressor(warm_start=warm_start, random_state=random_state)),
            # ('poly_features', PolynomialFeatures(degree=2)),
            # ('linear_regression', LinearRegression())
        ])
        model_pipline.fit(input_x_scaled, output_y)

        # Prepare the last rolling window of data for prediction
        test_x = np.array([numeric_sequence[-rolling_size:]])
        test_x_scaled = scaler.transform(test_x)

        # Predicting the next value
        pred_y = model_pipline.predict(test_x_scaled)
        return pred_y

    @staticmethod
    def random_forest_regressor_next_value(numeric_sequence: List[int]) -> int:
        """
        Predicts the next value in a sequence using a Random Forest Regressor.

        A Random Forest Regressor is a type of ensemble machine learning model that uses
        multiple decision trees to make predictions. It is particularly useful for regression
        tasks on complex datasets because it can capture non-linear relationships between
        variables. This function applies the model to a sequence of numbers to predict the
        next value based on the observed trend.

        :param numeric_sequence: A list or sequence of numbers to model.
        :return: The predicted next value in the sequence as an integer.
        """
        # Convert the numeric sequence into a numpy array and reshape for sklearn
        data = np.array(numeric_sequence).reshape(-1, 1)

        # Create an array representing time or the independent variable, reshaped as a column
        time_feature = np.array(range(len(data))).reshape(-1, 1)

        # Create a RandomForestRegressor model and fit it to the data
        model = RandomForestRegressor()
        model.fit(time_feature, data.ravel())  # Flatten the array to fit the model

        # Predict the next value in the sequence using the fitted model
        future_time = np.array([len(data)]).reshape(-1, 1)
        future_pred = model.predict(future_time)

        # Return the predicted value as an integer
        return CalculateUtil.real_round(future_pred[0])

    @staticmethod
    def relative_strength_index(numeric_sequence: List[int], period: int = 14) -> float:
        """
        Calculate the Relative Strength Index (RSI) using Exponential Moving Average (EMA).

        :param numeric_sequence: A list of prices for a particular stock or asset.
        :param period: The period over which to calculate the RSI, typically 14.
        :return: The calculated RSI value.
        """
        if len(numeric_sequence) < period:
            raise ValueError("Not enough data points to calculate RSI")

        deltas = [numeric_sequence[i + 1] - numeric_sequence[i] for i in range(len(numeric_sequence) - 1)]
        gains = [max(delta, 0) for delta in deltas]
        losses = [max(-delta, 0) for delta in deltas]

        # Initialize EMA with SMA for the first 'period'
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period

        # Apply EMA formula for gains and losses
        ema_factor = 2 / (period + 1)
        for i in range(period, len(deltas)):
            avg_gain = (gains[i] * ema_factor) + (avg_gain * (1 - ema_factor))
            avg_loss = (losses[i] * ema_factor) + (avg_loss * (1 - ema_factor))

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs)) if avg_loss != 0 else 100

        return rsi

    @staticmethod
    def seasonal_autoregressive_integrated_moving_average_next_value(numeric_sequence: List[int]) -> int:
        """
        Fit a Seasonal Autoregressive Integrated Moving Average (SARIMA) model to
        the provided time series data and predict the next value in the series.

        SARIMA models are used to forecast future points in a time series. They are
        capable of modeling complex seasonal patterns by incorporating both non-seasonal
        (ARIMA) and seasonal elements.

        :param numeric_sequence: A list of numerical values representing a time series.
        :return: The next integer value predicted by the SARIMA model.
        """
        # Convert the data to a numpy array for time series analysis
        timeseries = np.array(numeric_sequence)

        # Automatically discover the optimal order for the SARIMA model
        stepwise_model = auto_arima(timeseries, start_p=2, start_q=2,
                                    max_p=3, max_q=3, m=12,
                                    start_P=1, start_Q=1, max_P=3, max_Q=3,
                                    seasonal=True,
                                    d=1, D=1, trace=False,
                                    error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True)

        # Fit the SARIMA model to the time series data
        model = stepwise_model.fit(timeseries)

        # Predict the next value in the time series
        forecast = model.predict(n_periods=1)

        # Return the predicted value as an integer
        return CalculateUtil.real_round(forecast[0])
