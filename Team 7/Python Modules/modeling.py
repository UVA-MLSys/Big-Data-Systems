import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor, AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from xgboost import XGBRegressor
from skopt import BayesSearchCV
from skopt.space import Real, Integer, Categorical
from helper_functions import plot_model_performance, print_dict_imps

def train_models(df_selected, df, labels, feature_names, label_col_name="mvp_share"):
    """
    Train multiple regression models using Bayesian optimization, evaluate their performance,
    and save the best model.

    Parameters:
    -----------
    df_selected : pandas DataFrame
        The DataFrame containing the features used for training the models.
    
    df : pandas DataFrame
        The DataFrame containing the features used for stratifying and labeling.
        
    labels : array-like
        The target variable values.
        
    feature_names : list
        A list of feature names used for training.
        
    label_col_name : str, optional
        The name of the column containing the target variable in the DataFrame. Default is "mvp_share".

    Returns:
    --------
    trained_models : dict
        A dictionary containing the trained models as values, with their names as keys.
        
    results : dict
        A dictionary containing the evaluation results (MSE and R-squared) of the trained models,
        with the model names as keys.
        
    best_model_name : str
        The name of the best performing model.
        
    best_model : object
        The best performing model saved as a pickle file ('best_model.pkl').

    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df_selected, 
                                                        labels, 
                                                        test_size=0.2, 
                                                        stratify=df["Rank"], 
                                                        random_state=28)
    
    # Initialize models
    DTree = DecisionTreeRegressor(random_state=28)
    XTrees = ExtraTreesRegressor(random_state=28)
    Ada = AdaBoostRegressor(random_state=28)
    RF = RandomForestRegressor(random_state=28)
    GB = GradientBoostingRegressor(random_state=28)
    XGB = XGBRegressor(random_state=28)
    
    models = {
        "DTree": DTree,
        "XTrees": XTrees,
        "Ada": Ada,
        "RF": RF,
        "GB": GB,
        "XGB": XGB
    }
    
    # Define hyperparameter search spaces
    param_grids = {
        "DTree": {
            'max_depth': Integer(3, 10, prior='uniform'),
            'min_samples_split': Integer(2, 20, prior='uniform'),
            'min_samples_leaf': Integer(1, 10, prior='uniform'),
            'max_features': Categorical([None, 'log2', 'sqrt'])
        },
        "XTrees": {
            'n_estimators': Integer(100, 500, prior='uniform'),
            'max_depth': Integer(3, 10, prior='uniform'),
            'min_samples_split': Integer(2, 10, prior='uniform'),
            'min_samples_leaf': Integer(1, 7, prior='uniform'),
            'max_features': Categorical([None, 0.1, 1.0]),
            'bootstrap': Categorical([True, False])
        },
        "Ada": {
            'n_estimators': Integer(50, 500, prior='uniform'),
            'learning_rate': Real(0.01, 1.0),
            'loss': Categorical(['linear', 'square', 'exponential'])
        },
        "RF": {
            'n_estimators': Integer(200, 300),
            'max_features': Categorical(['log2', 'sqrt']),
            'max_depth': Integer(3, 15, prior='uniform'),
            'min_samples_split': Integer(2, 25, prior='uniform'),
            'min_samples_leaf': Integer(1, 12, prior='uniform'),
            'bootstrap': Categorical([True, False])
        },
        "GB": {
            'n_estimators': Integer(100, 300),
            'learning_rate': Real(0.05, 0.1, prior='uniform'),
            'max_depth': Integer(3, 15, prior='uniform'),
            'min_samples_split': Integer(2, 25, prior='uniform'),
            'min_samples_leaf': Integer(1, 12, prior='uniform'),
            'subsample': Real(0.6, 0.8, prior='uniform'),
            'max_features': Categorical(['log2', 'sqrt'])
        },
        "XGB": {
            'n_estimators': Integer(100, 500),
            'learning_rate': Real(0.01, 0.3, prior='uniform'),
            'max_depth': Integer(3, 10, prior='uniform'),
            'min_child_weight': Integer(1, 10),
            'subsample': Real(0.6, 1.0, prior='uniform'),
            'colsample_bytree': Real(0.6, 1.0, prior='uniform'),
            'gamma': Real(0, 0.5, prior='uniform'),
            'reg_alpha': Real(0, 1.0, prior='uniform'),
            'reg_lambda': Real(0, 1.0, prior='uniform')
        }
    }
    
    # Train models
    trained_models = {}
    for model_name, model in models.items():
        param_grid = param_grids[model_name]
        bayes_search = BayesSearchCV(estimator=model, 
                                     search_spaces=param_grid,
                                     n_iter=50, 
                                     scoring='r2', 
                                     cv=5,
                                     n_points=15,
                                     random_state=28, 
                                     n_jobs=-1)
        bayes_search.fit(X_train, y_train)
        trained_models[model_name] = bayes_search.best_estimator_
    
    # Evaluate models
    results = {}
    for model_name, model in trained_models.items():
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        results[model_name] = {"MSE": mse, "R-squared": r2}
    
    # Find the best model based on R-squared
    best_model_name = max(results, key=lambda x: results[x]['R-squared'])
    best_model = trained_models[best_model_name]
    # Save the best model
    joblib.dump(best_model, 'best_model.pkl')
    
    # Calculate feature importances
    feature_importances = {}
    for model_name, model in trained_models.items():
        importances = model.feature_importances_ if hasattr(model, 'feature_importances_') else None
        feature_importances[model_name] = {feature_names[i]: importances[i] for i in range(len(feature_names))}
    
    # Extract the model names, R-squared values, and MSE values from the results
    model_names = list(results.keys())
    r_sqs = [result["R-squared"] for result in results.values()]
    MSE_s = [result["MSE"] for result in results.values()]
    
    # Call the plotting function
    plot_model_performance(model_names, r_sqs, MSE_s)
    
    # Call the print_dict_imps function
    print_dict_imps(feature_importances)


    return trained_models, results, best_model_name, best_model