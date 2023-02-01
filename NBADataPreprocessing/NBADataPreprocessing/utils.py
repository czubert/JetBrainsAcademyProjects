import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from sklearn.impute import SimpleImputer
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder


class ReduceVIF(BaseEstimator, TransformerMixin):
    def __init__(self, thresh, impute=True, impute_strategy='median'):
        self.thresh = thresh

        if impute:
            self.imputer = SimpleImputer(strategy=impute_strategy)

    def fit(self, X, y=None):
        # ReduceVIF fit
        if hasattr(self, 'imputer'):
            self.imputer.fit(X)
        return self

    def transform(self, X, y=None):
        # ReduceVIF transform
        columns = X.columns.tolist()
        if hasattr(self, 'imputer'):
            X = pd.DataFrame(self.imputer.transform(X), columns=columns)
        return ReduceVIF.calculate_vif(X, self.thresh)

    @staticmethod
    def calculate_vif(X, thresh=0.5):
        dropped = True
        while dropped:
            variables = X.columns
            dropped = False
            vif = [variance_inflation_factor(X[variables].values, X.columns.get_loc(var)) for var in X.columns]

            max_vif = max(vif)
            if max_vif > thresh:
                maxloc = vif.index(max_vif)
                X = X.drop([X.columns.tolist()[maxloc]], axis=1)
                dropped = True
        return X


class MyOneHotEncoder(BaseEstimator, TransformerMixin):
    # classic OneHotEncoder, but returning DataFrame instead of NumPy array
    # It is made to keep the names of the columns
    def __init__(self):
        super().__init__()
        self._encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    def fit(self, X, y=None, cols=None):
        self._encoder.fit(X)
        return self

    def transform(self, X, y=None):
        X = X.copy()
        X = self._encoder.transform(X)
        X = pd.DataFrame(X, columns=self._encoder.get_feature_names_out())
        return X


class BackToDf(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        super().__init__()
        self._columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = pd.DataFrame(X, columns=self._columns)
        return df
