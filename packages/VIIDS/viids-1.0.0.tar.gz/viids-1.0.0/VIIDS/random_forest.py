from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pandas as pd

def train_random_forest_regressor(data, target_column, test_size=0.3, random_state=21, n_estimators=100):
    """
    Train a Random Forest Regressor model.

    Parameters:
    data: The input data.
    target_column: The name of the target column.
    test_size: The proportion of the dataset to include in the test split.
    random_state: Controls the shuffling applied to the data before applying the split.
    n_estimators: The number of trees in the forest.

    Returns:
    model (RandomForestRegressor): The trained Random Forest Regressor model.
    mse (float): The mean squared error of the model on the test set.
    r2
    """
    # Split the data into features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Initialize the Random Forest Regressor
    # Parameters Can Include:
    # n_estimators, max_depth, min_samples_splits, min_samples_leaf, etc(use as needed)
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate the mean squared error
    mse = mean_squared_error(y_test, y_pred)

    # Calculate the R-squared score
    r2 = r2_score(y_test, y_pred)

    return model, mse, r2

