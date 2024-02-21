from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


#RandomForestRegressor is selected because
#High Accuracy: Random forests are known for their high accuracy. They can capture complex relationships between features and target variables, making them suitable for a wide range of regression problems.
# Robustness to Overfitting: Unlike some other algorithms (like decision trees), random forests are less prone to overfitting, especially when trained with a large number of trees. By averaging predictions from multiple trees, random forests can generalize well to unseen data.
# Handles Non-linear Relationships: Random forests can capture non-linear relationships between features and target variables effectively. They do not require feature scaling or transformation, making them suitable for datasets with mixed feature types.
# Feature Importance: Random forests provide a measure of feature importance, indicating which features have the most significant impact on the predictions. This information can help with feature selection and interpretation of the model.
# Handles Missing Values: Random forests can handle missing values in the dataset without the need for imputation. They use surrogate splits to make predictions even when some values are missing.
# Outlier Robustness: Random forests are robust to outliers and noise in the data. Outliers have less impact on the overall model performance because predictions are based on an ensemble of trees.
# Parallelization: Training multiple decision trees in a random forest can be parallelized, making it efficient to train on large datasets and take advantage of multi-core processors.
# Reduces Variance: By aggregating predictions from multiple trees, random forests reduce the variance of the model compared to individual decision trees. This leads to more stable and reliable predictions.
# No Assumptions About Data: Random forests make no assumptions about the distribution or linearity of the data, making them versatile and applicable to a wide range of datasets.

class DurationPredictorCalculatedWorker():
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def set_data(self, data):
        self.df = pd.DataFrame(data)

    #Modify data to fit ML
    def preprocess_data(self):
        self.df['time'] = self.df['time'].apply(self._time_to_minutes)
        self.remove_outliers()

    #removing data that dose not fit (usual time 48,55, 40, 60 , 10000 - it would remove 10000)
    def remove_outliers(self, z_threshold=3):
        # Calculate z-scores for 'calculated_duration'
        z_scores = (self.df['calculated_duration'] - self.df['calculated_duration'].mean()) / self.df['calculated_duration'].std()
        # Remove data points with z-scores greater than threshold
        self.df = self.df[np.abs(z_scores) <= z_threshold]

    #modifies '13:11' -> 791 for ML
    def _time_to_minutes(self, time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    # trains the modal
    def train_model(self):
        X = self.df[['weekday', 'time', 'calculated_duration']]
        y = self.df['actual_duration']
        # split data for training and testing
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    #evaluate and store mean_squared_error for valuating if this result should be used
    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        self.mse = mean_squared_error(self.y_test, y_pred)
        #print(f"Mean Squared Error: {mse}")

    #predict result from given inputs
    def predict_duration(self, weekday, time, estimated_duration):
        time_in_minutes = self._time_to_minutes(time)
        predicted_actual_duration = self.model.predict([[weekday, time_in_minutes, estimated_duration]])
        return predicted_actual_duration[0]




class DurationPredictorWorker:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def set_data(self, data):
        self.df = pd.DataFrame(data)
        # time = datetime_obj.time()

    def preprocess_data(self):
        self.df['time'] = self.df['time'].apply(self._time_to_minutes)
        self.remove_outliers()

    def _time_to_minutes(self, time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def remove_outliers(self, z_threshold=3):
        # Calculate z-scores for 'duration'
        z_scores = (self.df['duration'] - self.df['duration'].mean()) / self.df['duration'].std()
        # Remove data points with z-scores greater than threshold
        self.df = self.df[np.abs(z_scores) <= z_threshold]

    def train_model(self):
        X = self.df[['weekday', 'time']]
        y = self.df['duration']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        self.mse = mean_squared_error(self.y_test, y_pred)
        # print(f"Mean Squared Error: {mse}")

    def predict_next_duration(self, weekday, time):
        time_in_minutes = self._time_to_minutes(time)
        predicted_duration = self.model.predict([[weekday, time_in_minutes]])
        return predicted_duration[0]
