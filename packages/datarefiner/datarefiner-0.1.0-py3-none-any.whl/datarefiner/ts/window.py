#!/usr/bin/env python
# Created by "Thieu" at 13:42, 24/07/2024 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import pandas as pd
import numpy as np


class SlidingTransformer:
    def __init__(self, lags=(1, 2), future_steps=(0, 1), dropnan=True):
        # Convert single integer inputs to lists
        if isinstance(lags, int):
            self.lags = [lags]
        else:
            self.lags = lags
        if isinstance(future_steps, int):
            self.future_steps = [future_steps]
        else:
            self.future_steps = future_steps
        self.dropnan = dropnan
        self.data = None

    def transform(self, data):
        """
        Perform sliding window technique on data.

        Parameters:
        X (array-like): The input data to transform.

        Returns:
        np.array: The supervised dataset
        """
        cols = list()
        names = ["var"]
        col_names = list()
        if isinstance(data, (list, tuple, np.ndarray)):
            data = np.array(data)
            if data.ndim == 1:
                names = [f"var"]
            else:
                names = [f'var{j + 1}' for j in range(data.shape[1])]
        if isinstance(data, pd.Series):
            if data.name is None:
                names = ["var"]
            else:
                names = [data.name]
            data = data.values
        if isinstance(data, pd.DataFrame):
            if data.columns is None:
                names = [f'var{j + 1}' for j in range(data.values.ndim)]
            else:
                names = data.columns
            data = data.values
        n_vars = len(names)
        df = pd.DataFrame(data, columns=names)
        self.data = df.copy()

        # Input sequence (t-n, ... t-1)
        for i in self.lags:
            cols.append(df.shift(i))
            col_names += [f'{names[j]}(t-{i})' for j in range(n_vars)]

        # Forecast sequence (t, t+1, ... t+n)
        for i in self.future_steps:
            cols.append(df.shift(-i))
            if i == 0:
                col_names += [f'{names[j]}(t)' for j in range(n_vars)]
            else:
                col_names += [f'{names[j]}(t+{i})' for j in range(n_vars)]

        # Combine all columns
        agg = pd.concat(cols, axis=1)
        agg.columns = col_names

        # Drop rows with NaN values
        if self.dropnan:
            agg.dropna(inplace=True)

        return agg

    def reconnect_predictions(self, predictions, start_index=None):
        """
        Reconnect the predicted data to the original data for each column.

        Parameters:
        predictions (array-like): The least steps predicted data after training the model.

        Returns:
        pd.DataFrame: The original data.
        """
        data = self.data.copy()
        if start_index is None:
            start_index = len(self.data) - (min(self.future_steps) + 1) - len(predictions)         # future steps start at 0.
        # Replace the part of the series with predictions
        for i, pred in enumerate(predictions):
            data[start_index + i] = pred
        return data


class RollingStatisticTransformer:
    def __init__(self, lags=(1, 2), future_steps=(0, 1), statistics=None):
        self.lags = lags
        self.future_steps = future_steps
        self.statistics = statistics if statistics is not None else ['mean']
        self.valid_statistics = ['mean', 'std', 'sum', 'min', 'max', "variance", "median", "kurtosis", "skew"]

        for stat in self.statistics:
            if stat not in self.valid_statistics:
                raise ValueError(f"Invalid statistic '{stat}'. Choose from {self.valid_statistics}")

    def transform(self, data):
        if isinstance(data, (list, tuple, np.ndarray)):
            data = np.array(data)
            if data.ndim == 1:
                names = [f"var"]
            else:
                names = [f'var{j + 1}' for j in range(data.shape[1])]
        if isinstance(data, pd.Series):
            if data.name is None:
                names = ["var"]
            else:
                names = [data.name]
            data = data.values
        if isinstance(data, pd.DataFrame):
            if data.columns is None:
                names = [f'var{j + 1}' for j in range(data.values.ndim)]
            else:
                names = data.columns
            data = data.values
        data = pd.DataFrame(data, columns=names)
        features = pd.DataFrame(index=data.index)
        labels = pd.DataFrame(index=data.index)

        # Apply transformations to each column
        for col in data.columns:
            col_features, col_labels = self._transform_series(data[col], col)
            features = pd.concat([features, col_features], axis=1)
            labels = pd.concat([labels, col_labels], axis=1)

        # Drop rows with NaN values resulting from the lags and future steps
        min_lag = max(self.lags)
        max_future_step = max(self.future_steps)
        valid_index = features.index[min_lag:-max_future_step]

        return features.loc[valid_index], labels.loc[valid_index]

    def _transform_series(self, series, col_name):
        # Create lagged features
        col_features = pd.DataFrame(index=series.index)
        for lag in self.lags:
            col_features[f'{col_name}_lag_{lag}'] = series.shift(lag)

        # Compute rolling statistics on the lagged features
        for stat in self.statistics:
            if stat == 'mean':
                col_features[f'{col_name}_mean'] = col_features.mean(axis=1)
            elif stat == 'std':
                col_features[f'{col_name}_std'] = col_features.std(axis=1)
            elif stat == 'sum':
                col_features[f'{col_name}_sum'] = col_features.sum(axis=1)
            elif stat == 'min':
                col_features[f'{col_name}_min'] = col_features.min(axis=1)
            elif stat == 'max':
                col_features[f'{col_name}_max'] = col_features.max(axis=1)
            elif stat == "median":
                col_features[f'{col_name}_median'] = col_features.median(axis=1)
            elif stat == "variance":
                col_features[f'{col_name}_variance'] = col_features.var(axis=1)
            elif stat == "kurtosis":
                col_features[f'{col_name}_kurtosis'] = col_features.kurt(axis=1)
            elif stat == "skew":
                col_features[f'{col_name}_skew'] = col_features.skew(axis=1)

        # Generate future steps labels
        col_labels = pd.DataFrame(index=series.index)
        for step in self.future_steps:
            col_labels[f'{col_name}_future_step_{step}'] = series.shift(-step)

        return col_features, col_labels


class ExpandingStatisticTransformer:
    def __init__(self, future_steps=(1, 3), statistics=None):
        self.future_steps = future_steps
        self.statistics = statistics if statistics is not None else ['mean']
        self.valid_statistics = ['mean', 'std', 'sum', 'min', 'max', "variance", "median", "kurtosis", "skew"]

        for stat in self.statistics:
            if stat not in self.valid_statistics:
                raise ValueError(f"Invalid statistic '{stat}'. Choose from {self.valid_statistics}")

    def transform(self, data):
        if isinstance(data, (list, tuple, np.ndarray)):
            data = np.array(data)
            if data.ndim == 1:
                names = [f"var"]
            else:
                names = [f'var{j + 1}' for j in range(data.shape[1])]
        if isinstance(data, pd.Series):
            if data.name is None:
                names = ["var"]
            else:
                names = [data.name]
            data = data.values
        if isinstance(data, pd.DataFrame):
            if data.columns is None:
                names = [f'var{j + 1}' for j in range(data.values.ndim)]
            else:
                names = data.columns
            data = data.values
        data = pd.DataFrame(data, columns=names)
        features = pd.DataFrame(index=data.index)
        labels = pd.DataFrame(index=data.index)

        # Apply transformations to each column
        for col in data.columns:
            col_features, col_labels = self._transform_series(data[col], col)
            features = pd.concat([features, col_features], axis=1)
            labels = pd.concat([labels, col_labels], axis=1)

        # Drop rows with NaN values resulting from the expanding calculations and future steps
        max_future_step = max(self.future_steps)
        features.dropna(inplace=True)
        valid_index = features.index[:-max_future_step]
        return features.loc[valid_index], labels.loc[valid_index]

    def _transform_series(self, series, col_name):
        col_features = pd.DataFrame(index=series.index)

        # Compute expanding statistics on the series
        for stat in self.statistics:
            if stat == 'mean':
                col_features[f'{col_name}_mean'] = series.expanding().mean()
            elif stat == 'std':
                col_features[f'{col_name}_std'] = series.expanding().std()
            elif stat == 'sum':
                col_features[f'{col_name}_sum'] = series.expanding().sum()
            elif stat == 'min':
                col_features[f'{col_name}_min'] = series.expanding().min()
            elif stat == 'max':
                col_features[f'{col_name}_max'] = series.expanding().max()
            elif stat == "median":
                col_features[f'{col_name}_median'] = series.expanding().median()
            elif stat == "variance":
                col_features[f'{col_name}_variance'] = series.expanding().var()
            elif stat == "kurtosis":
                col_features[f'{col_name}_kurtosis'] = series.expanding().kurt()
            elif stat == "skew":
                col_features[f'{col_name}_skew'] = series.expanding().skew()

        # Generate future steps labels
        col_labels = pd.DataFrame(index=series.index)
        for step in self.future_steps:
            col_labels[f'{col_name}_future_step_{step}'] = series.shift(-step)

        return col_features, col_labels
