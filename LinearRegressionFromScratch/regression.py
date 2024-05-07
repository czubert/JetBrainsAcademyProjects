import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class CustomLinearRegression:

    def __init__(self, *, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coefficient = np.array([])
        self.intercept = 0.0

    def fit(self, X, y):
        if self.fit_intercept:
            X = np.column_stack((np.ones_like(X[:, 0]), X))  # Add column of ones for intercept
        XtX = np.dot(X.T, X)
        Xty = np.dot(X.T, y)
        self.coefficient = np.dot(np.linalg.inv(XtX), Xty)
        if self.fit_intercept:
            self.intercept = self.coefficient[0]
            self.coefficient = self.coefficient[1:]
        else:
            self.intercept = 0.0

    def predict(self, X):
        if self.fit_intercept:
            X = np.column_stack((np.ones_like(X[:, 0]), X))  # Add column of ones for intercept
        return np.dot(X, np.concatenate(([self.intercept], self.coefficient)))  # Return predictions

    def r2_score(self, y, yhat):
        ybar = np.mean(y)
        ss_tot = np.sum((y - ybar) ** 2)
        ss_res = np.sum((y - yhat) ** 2)
        return 1 - (ss_res / ss_tot)

    def rmse(self, y, yhat):
        mse = np.mean((y - yhat) ** 2)
        return np.sqrt(mse)

# Data
f1 = np.array([2.31, 7.07, 7.07, 2.18, 2.18, 2.18, 7.87, 7.87, 7.87, 7.87])
f2 = np.array([65.2, 78.9, 61.1, 45.8, 54.2, 58.7, 96.1, 100.0, 85.9, 94.3])
f3 = np.array([15.3, 17.8, 17.8, 18.7, 18.7, 18.7, 15.2, 15.2, 15.2, 15.2])
y = np.array([24.0, 21.6, 34.7, 33.4, 36.2, 28.7, 27.1, 16.5, 18.9, 15.0])

# Initialize and fit the CustomLinearRegression model
regCustom = CustomLinearRegression(fit_intercept=True)
X = np.column_stack((f1, f2, f3))  # Create data matrix
regCustom.fit(X, y)

# Predict y
y_pred_custom = regCustom.predict(X)

# Calculate RMSE and R2 for CustomLinearRegression
RMSE_custom = regCustom.rmse(y, y_pred_custom)
R2_custom = regCustom.r2_score(y, y_pred_custom)

# Initialize and fit the LinearRegression model from sklearn
regSci = LinearRegression(fit_intercept=True)
regSci.fit(X, y)

# Predict y with LinearRegression
y_pred_sci = regSci.predict(X)

# Calculate RMSE and R2 for LinearRegression
RMSE_sci = np.sqrt(mean_squared_error(y, y_pred_sci))
R2_sci = r2_score(y, y_pred_sci)

# Calculate the differences in intercept, coefficient, RMSE, and R2 values
differences = {
    'Intercept': regSci.intercept_ - regCustom.intercept,
    'Coefficient': regSci.coef_ - regCustom.coefficient,
    'R2': R2_sci - R2_custom,
    'RMSE': RMSE_sci - RMSE_custom
}

print(differences)
