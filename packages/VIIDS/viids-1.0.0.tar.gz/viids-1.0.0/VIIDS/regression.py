from sklearn.metrics import r2_score
from sklearn.model_selection import KFold 
from sklearn.feature_selection import RFE

def recursive_select(x_train, x_test, y_train, y_test, feature_num, selector, step=1):
    '''
    Function to do recursive selection takes the training and testing sets, number and features and the sklearn estimator you want
    Returns the features selected and its r2 value

    Helper function for recursive_select_feature_set() not meant to be used directly
    '''

    if feature_num >= x_train.shape[1]: raise("Error, too many features for this set") # Incase this function is invoked directly.
    x_train_c, x_test_c, y_train_c, y_test_c = x_train.copy(), x_test.copy(), y_train.copy(), y_test.copy() 

    RFE_selector = RFE(estimator=selector, n_features_to_select=feature_num, step=step)
    RFE_selector = RFE_selector.fit(x_train_c, y_train_c)
    # Uses the RFE slector tool to do the recusive fit for the selected number of variables

    sel_x_train_c = RFE_selector.transform(x_train_c)
    sel_x_test_c = RFE_selector.transform(x_test_c)

    selector.fit(sel_x_train_c, y_train_c)
    r2_preds = selector.predict(sel_x_test_c)
    
    r2 = round(r2_score(y_test_c, r2_preds), 3)
    # Calculates our r2ed value for this run of recurisve_select()
    
    return((x_train_c.columns[RFE_selector.support_], r2))

def recursive_select_feature_set(x_train, y_train, selector, step=1, k=5):
    '''
    Returns a list of selected features and r2 values for each possible feature size using a given sklearn estimator
    Uses recursive_select() with cross validation
    '''
    feature_range = list()
    for i in range(x_train.shape[1] - 1):
        feature_range.append(i + 1)
    # Makes a list of all possible number of features

    results = list()
    for num in feature_range:
        results.append(cross_val_kfolds(x_train, y_train, num, selector, step, k))
    # grabs the feature count and R2ed value for each round

    return results

def cross_val_kfolds(x_train_org, y_train_org, num, selector, step, k):
    '''
    Helper function for recursive_select_feature_set() which uses kfolds to cross validate
    this is done to void dipping into our testing data

    Not meant to be used directly
    '''

    kf = KFold(n_splits=k, shuffle=True, random_state=21) # sets the KFold object

    feature_set = ''
    r2_scores_max = 0

    for i_train, i_test in kf.split(x_train_org, y_train_org):

        x_train = x_train_org.drop(x_train_org.index[i_test])
        x_test = x_train_org.drop(x_train_org.index[i_train])
        y_train = y_train_org.drop(y_train_org.index[i_test])
        y_test = y_train_org.drop(y_train_org.index[i_train])
        #splits the orginal training data into this KFolds rounds particular train test split

        feature_set, r2 = recursive_select(x_train, x_test, y_train, y_test, num, selector, step)
        if r2 > r2_scores_max: r2_scores_max = r2
        # Gets the max R2ed for each KFold validation
        
    return feature_set, r2_scores_max