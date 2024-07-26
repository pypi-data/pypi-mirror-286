#!/usr/bin/env python
# Created by "Thieu" at 10:28, 24/07/2024 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np


class DifferenceScaler:
    def __init__(self, order=1):
        """
        Initialize the Differencing Scaler with order.

        Parameters:
        d (int): The order of differencing.
        """
        self.order = order
        self.initial_values = []
        self.ndim = 1

    def transform(self, X):
        """
        Perform differencing on X.

        Parameters:
        X (array-like): The input data to transform.

        Returns:
        np.array: The differenced data.
        """
        X = np.array(X)
        if X.ndim == 1:
            self.ndim = 1
            X = np.reshape(X, (-1, 1))
        else:
            self.ndim = X.ndim

        # Store the initial values required for inverse transformation for each column.
        self.initial_values = []
        for col in range(X.shape[1]):
            col_initial_values = []
            current_series = X[:, col]
            for i in range(self.order):
                col_initial_values.append(current_series[0])
                current_series = np.diff(current_series)
            self.initial_values.append(col_initial_values)

        # Perform differencing on each column of the data.
        differenced = np.zeros((X.shape[0] - self.order, X.shape[1]))
        for col in range(X.shape[1]):
            col_data = X[:, col]
            for _ in range(self.order):
                col_data = np.diff(col_data)
            differenced[:, col] = col_data
        return differenced if self.ndim != 1 else differenced.ravel()

    def inverse_transform(self, X):
        """
        Inverse transform the differenced data to the original data for each column.

        Parameters:
        X (array-like): The differenced data to inverse transform.

        Returns:
        np.array: The original data.
        """
        X = np.array(X)
        if self.ndim == 1:
            X = np.reshape(X, (-1, 1))

        recovered = np.zeros((X.shape[0] + self.order, X.shape[1]))
        for col in range(X.shape[1]):
            col_data = X[:, col]
            for i in range(self.order):
                initial_value = self.initial_values[col][self.order - 1 - i]
                col_data = np.concatenate(([initial_value], col_data)).cumsum()
            recovered[:, col] = col_data
        return recovered if self.ndim != 1 else recovered.ravel()
