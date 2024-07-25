from sklearn.model_selection import GridSearchCV

def perform_grid_search(model, param_grid, X_train, y_train, cv=5, scoring='neg_mean_squared_error'):
    """
    Perform Grid Search with Cross-Validation to find the best hyperparameters.

    Parameters:
    model: The machine learning model to be tuned
    param_grid: The parameter grid to search over
    X_train (pd.DataFrame): The training features
    y_train (pd.Series): The training target
    cv: Number of cross-validation folds
    scoring: Scoring metric to use

    Returns:
    best_model: The model with the best found parameters
    best_params: The best found parameters
    best_score: The best score achieved
    """

    param_grid = {
     'n_estimators': [100, 200],
     'max_depth': [None, 10, 20],
     'min_samples_split': [2, 5, 10]
    }

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=cv, scoring=scoring, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    return best_model, best_params, best_score


from sklearn.model_selection import cross_val_score, KFold

def perform_k_fold_cv(model, X, y, k=5, scoring='neg_mean_squared_error'):
    """
    Perform K-Fold Cross-Validation.

    Parameters:
    model: The machine learning model to be evaluated.
    X: The features
    y: The target
    k: Number of folds
    scoring: Scoring metric to use

    Returns:
    scores: List of scores for each fold
    mean_score: Mean score across all folds
    """
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=kf, scoring=scoring, n_jobs=-1)
    
    mean_score = scores.mean()

    return scores, mean_score
