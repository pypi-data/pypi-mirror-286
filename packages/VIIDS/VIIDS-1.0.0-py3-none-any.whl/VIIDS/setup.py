import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split

def model_split(x, y):
    '''
    returns a training and testing set using sklearns train_test_split fucntion using a test size of 0.3 and a random state of 21
    '''
    return train_test_split(x, y, test_size = 0.3, shuffle = True, random_state = 21)

def predict(X, model):
    '''the built-in get_prediction tool returns an array, so we need to convert to a dataframe'''
    predictions_df = pd.DataFrame(model.get_prediction(X).predicted, columns=['y_hat'], index=X.index)
    return predictions_df['y_hat']

def mse(y, y_hat):
    '''gets the mean squared error'''
    # calculate the residual error for each individual record
    resid = y - y_hat
    # square the residual (hence "squared error")
    sq_resid = resid**2
    # calculate the sum of squared errors
    SSR = sum(sq_resid)
    # divide by the number of records to get the mean squared error
    MSE = SSR / y.shape[0]
    return MSE

def csvtos(filename):
    """
    Converts a .csv file to a usable pandas series.
        
        Parameter:
            filename: String containing the .csv filename

        Returns:
            series: A pandas series containing the .csv file's content.
    """
    
    if ".csv" not in filename:
        filename = filename + ".csv"

    dataframe = pd.read_csv(filename, index_col=0)
    series = dataframe.columns[0]
    series = dataframe.iloc[:, 0]

    filename = filename.replace(".csv", "")
    series.name = filename

    return series

def stocsv(series):
    """
    Downloads a pandas series as a .csv file in the current location.

        Parameter:
            series: The pandas series to be downloaded
    """
    
    series.to_csv(series.name, index=True, header=True)
