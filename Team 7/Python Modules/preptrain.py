import pandas as pd
import numpy as np
import warnings
from skopt import BayesSearchCV
from skopt.space import Categorical, Real, Integer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import f_regression, SelectFromModel, RFE, RFECV, mutual_info_regression
from sklearn.cluster import FeatureAgglomeration
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, mutual_info_score
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn import metrics, linear_model
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.inspection import permutation_importance
from sklearn.tree import DecisionTreeRegressor
from sklearn.exceptions import ConvergenceWarning
from xgboost import XGBRegressor
from scipy.stats import randint

def preprocess_and_train(df, df_last, labels):
    """
    Preprocesses the data and trains various regression models for feature selection.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing features.

    df_last : pandas.DataFrame
        DataFrame for which predictions are to be made.

    labels : array-like
        Target variable.

    Returns:
    --------
    tuple
        A tuple containing:
        - List of top features selected by each model (features_rf, features_Dtree, features_pca,
          features_rfecv, features_gbm, features_svr, features_Xtrees, features_Ada, features_XGB).
        - Preprocessed training and testing data (X_train, X_test, y_train, y_test).
        - Dictionary containing feature importances for each model (feature_importances).
    """
    # Define numeric columns excluding "Pos"
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df, 
                                                        labels, 
                                                        test_size=0.2, 
                                                        shuffle=True, 
                                                        random_state=28)

    # Define preprocessing steps
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, ['Pos'])])

    # Preprocess training and testing data
    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)
    df_last_preprocessed = preprocessor.transform(df_last)

    # Extract feature names
    header_names = [col.split("__")[1] if "__" in col else col for col in preprocessor.get_feature_names_out()]

    # Dictionaries to store feature importances
    feature_importances = {}

####################################################################################################
                                        #########################
                                        ### FEATURE SELECTION ###
                                        #########################
####################################################################################################

    ###############################
    ### Random Forest Regressor ###
    ###############################
    
    # Define the hyperparameter grid
    param_grid_rf = {
        'n_estimators': Integer(200, 300),              # No. of trees in the forest
        'max_features': Categorical(['log2', 'sqrt']),  # No. of features to consider at every split
        'max_depth': Categorical([10, 20]),             # Max depth of the trees
        'min_samples_split': Integer(2, 5),             # Min no. of samples required to split an internal node
        'min_samples_leaf': Integer(1, 5),              # Min no. of samples required to be at a leaf node
        'bootstrap': Categorical([True, False])         # Method to select samples for training each tree
    }
    # Initialize RandomForestRegressor
    rf = RandomForestRegressor(random_state=28, n_jobs=-1)
    # Initialize BayesSearchCV
    bayes_search_rf = BayesSearchCV(estimator=rf, 
                                    search_spaces=param_grid_rf, 
                                    n_iter=50, 
                                    scoring='r2', 
                                    cv=5, 
                                    n_points=10,
                                    random_state=28, 
                                    n_jobs=-1)
    
    # Perform BayesSearchCV
    bayes_search_rf.fit(X_train_preprocessed, y_train)
    # Get the best hyperparameters
    best_params_rf = bayes_search_rf.best_params_
    # Get the best model
    best_rf = bayes_search_rf.best_estimator_
    # Calculate feature importances
    importances_rf = best_rf.feature_importances_
    # Get the indices of top features based on feature importances
    indices_rf = np.argsort(importances_rf)[::-1][:10]
    # Get the names of top features based on feature importances
    features_rf = [header_names[i] for i in indices_rf]
    # Store feature importances
    feature_importances['Random Forest'] = dict(zip(features_rf, importances_rf))

####################################################################################################

    ##############################
    ### DecisionTree Regressor ###
    ##############################
    
    # Define the hyperparameter search space for DecisionTreeRegressor
    param_grid_Dtree = {
        'max_depth': Categorical([3, 10]),              # Max depth of the tree
        'min_samples_split': Integer(2, 20),            # Min no. of samples required to split an internal node
        'min_samples_leaf': Integer(1, 10),             # Min no. of samples required to be at a leaf node
        'max_features': Categorical(['log2', 'sqrt']),  # No. of features to consider at every split
    }
    # Initialize DecisionTreeRegressor
    Dtree = DecisionTreeRegressor(random_state=28)
    # Initialize BayesSearchCV
    bayes_search_Dtree = BayesSearchCV(estimator=Dtree,
                                      search_spaces=param_grid_Dtree,
                                      n_iter=100,
                                      scoring='r2',
                                      cv=5,
                                      n_points=10,
                                      random_state=28,
                                      n_jobs=-1)
    
    # Perform Bayesian Optimization
    bayes_search_Dtree.fit(X_train_preprocessed, y_train)
    # Get the best hyperparameters
    best_params_Dtree = bayes_search_Dtree.best_params_
    # Get the best model
    best_Dtree = bayes_search_Dtree.best_estimator_
    # Calculate feature importances
    importances_Dtree = best_Dtree.feature_importances_
    # Get the indices of top features based on feature importances
    indices_Dtree = np.argsort(importances_Dtree)[::-1][:10]
    # Get the names of top features based on feature importances
    features_Dtree = [header_names[i] for i in indices_Dtree]
    # Store feature importances
    feature_importances['Decision Tree'] = dict(zip(features_Dtree, importances_Dtree))

####################################################################################################

    ####################################
    ### Principal Component Analysis ###
    ####################################
    pca = PCA(n_components=10, random_state=28)
    pca.fit(X_train_preprocessed)
    X_train_pca = pca.transform(X_train_preprocessed)
    features_pca_indices = np.argsort(np.abs(pca.components_), axis=1)[:, -10:]
    features_pca = []
    selected_components = np.abs(pca.components_)[:, features_pca_indices[0]]  # Absolute values of components
    # Get the original feature names corresponding to selected principal components
    for i, component_indices in enumerate(features_pca_indices):
        original_features = [header_names[idx] for idx in component_indices]
        features_pca.append(original_features)
    
    # Store selected features and their absolute component values in the feature_importances dictionary
    selected_features = features_pca[0]
    selected_components = selected_components[0]
    feature_importances['PCA'] = dict(zip(selected_features, selected_components))

####################################################################################################

    ###########################################
    ### Recursive Feature Elimination w/ CV ###
    ###########################################

    # Define the hyperparameter grid
    param_grid_gb = {
        'n_estimators': Integer(100, 300),                  # No. of boosting stages
        'learning_rate': Real(0.05, 0.1, prior='uniform'),  # Learning rate
        'max_depth': Categorical([3, 5]),                   # Max depth of individual trees
        'min_samples_split': Integer(2, 5),                 # Min no. of samples required to split an internal node
        'min_samples_leaf': Integer(1, 2),                  # Min no. of samples required to be at a leaf node
        'subsample': Real(0.6, 0.8, prior='uniform'),       # Fraction of samples used to fit the individual base learners
        'max_features': Categorical(['log2', 'sqrt'])       # No. of features to consider when looking for the best split
    }
    # Create the GradientBoostingRegressor estimator
    estimator_gb = GradientBoostingRegressor(random_state=28)
    # Create the BayesSearchCV object for GradientBoostingRegressor
    bayes_search_gb = BayesSearchCV(estimator=estimator_gb, 
                                    search_spaces=param_grid_gb, 
                                    n_iter=50,
                                    cv=5,
                                    n_points=10,
                                    random_state=28,
                                    n_jobs=-1)
    # Fit the BayesSearchCV to the preprocessed training data
    bayes_search_gb.fit(X_train_preprocessed, y_train)
    # Get the best GradientBoostingRegressor estimator from the BayesSearchCV
    best_gb_estimator = bayes_search_gb.best_estimator_
    # Create the RFECV estimator using the best GradientBoostingRegressor estimator
    selector_rfecv = RFECV(best_gb_estimator, step=5, cv=5, n_jobs=-1)
    # Fit the RFECV estimator to the preprocessed training data
    selector_rfecv.fit(X_train_preprocessed, y_train)
    # Get the selected indices from RFECV
    selected_indices_rfecv = selector_rfecv.get_support(indices=True)
    # Get the indices of top features based on mean test score
    features_rfecv_indices = np.argsort(selector_rfecv.cv_results_['mean_test_score'])[::-1][:10]
    # Get the names of top features based on mean test score
    features_rfecv = [header_names[i] for i in features_rfecv_indices]

####################################################################################################

    ###################################
    ### Gradient Boosting Regressor ###
    ###################################

    # Define the parameter grid for GradientBoostingRegressor
    param_grid_gb = {
        'n_estimators': Integer(100, 300),                  # No. of boosting stages
        'learning_rate': Real(0.05, 0.1, prior='uniform'),  # Learning rate
        'max_depth': Categorical([3, 5]),                   # Max depth of the individual trees
        'min_samples_split': Integer(2, 5),                 # Min no. of samples required to split an internal node
        'min_samples_leaf': Integer(1, 2),                  # Min no. of samples required to be at a leaf node
        'subsample': Real(0.6, 0.8, prior='uniform'),       # Fraction of samples used to fit individual base learners
        'max_features': Categorical(['log2', 'sqrt'])       # No. of features to consider when looking for the best split
    }
    
    # Create the GradientBoostingRegressor estimator
    gbm = GradientBoostingRegressor(random_state=28)
    # Create the BayesSearchCV object for GradientBoostingRegressor
    bayes_search_gb = BayesSearchCV(estimator=gbm, 
                                    search_spaces=param_grid_gb, 
                                    n_iter=50, 
                                    scoring='r2', 
                                    cv=5,
                                    n_points=10,
                                    n_jobs=-1,
                                    random_state=28)
    # Fit the BayesSearchCV to the preprocessed training data
    bayes_search_gb.fit(X_train_preprocessed, y_train)
    # Get the best GradientBoostingRegressor estimator from the BayesSearchCV
    best_gbm_estimator = bayes_search_gb.best_estimator_
    # Get the feature importances from the best GradientBoostingRegressor estimator
    importances_gbm = best_gbm_estimator.feature_importances_
    # Get the indices of top features based on feature importances
    indices_gbm = np.argsort(importances_gbm)[::-1][:10]
    # Get the names of top features based on feature importances
    features_gbm = [header_names[i] for i in indices_gbm]
    # Store feature importances
    feature_importances['GBM'] = dict(zip(features_gbm, importances_gbm))

####################################################################################################

    ################################
    ### Support Vector Regressor ###
    ################################

    # Define the parameter grid for SVR
    param_grid_svr = {
        'kernel': Categorical(['linear', 'poly']),   # Vary the kernel types
        'C': Real(0.1, 1.0, prior='uniform'),        # Vary the regularization parame
        'gamma': Categorical(['scale', 'auto'])      # Vary the gamma parame
    }
    # Create the SVR estimator
    svr = SVR()
    # Suppress ConvergenceWarnings during optimization
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        
        # Create the BayesSearchCV object for SVR
        bayes_search_svr = BayesSearchCV(estimator=svr, 
                                         search_spaces=param_grid_svr, 
                                         cv=5,
                                         n_points=10,
                                         n_jobs=-1,
                                         random_state=28,
                                         verbose=False)
        # Fit the BayesSearchCV to the preprocessed training data
        bayes_search_svr.fit(X_train_preprocessed, y_train)
    
    # Get the best SVR estimator from the BayesSearchCV
    best_svr_estimator = bayes_search_svr.best_estimator_
    # Calculate permutation importance using the best SVR estimator
    perm_importance = permutation_importance(best_svr_estimator, 
                                             X_train_preprocessed, 
                                             y_train, 
                                             n_repeats=3, 
                                             random_state=28)
    # Get the indices of top features based on permutation importance
    features_svr_indices = np.argsort(perm_importance.importances_mean)[::-1][:10]
    # Get the names of top features based on permutation importance
    features_svr = [header_names[i] for i in features_svr_indices]
    # Store feature importances
    feature_importances['SVR'] = dict(zip(features_svr, perm_importance.importances_mean))

####################################################################################################

    ############################
    ### ExtraTrees Regressor ###
    ############################
    
    # Define the hyperparameter grid
    param_grid_Xtrees = {
        'n_estimators': Integer(100, 500),          # No. of trees in the forest
        'max_depth': Categorical([3, 10]),          # Max depth of each tree
        'min_samples_split': Integer(2, 20),        # Min no. of samples required to split an internal node
        'min_samples_leaf': Integer(1, 10),         # Min no. of samples required to be at a leaf node
        'max_features': Categorical([0.1, 1.0]),    # No. of features to consider when looking for the best split
        'bootstrap': Categorical([True, False])     # Whether to use bootstrap samples when building trees
    }
    # Initialize ExtraTreesRegressor
    Xtrees = ExtraTreesRegressor(random_state=28, n_jobs=-1)
    # Initialize BayesSearchCV
    bayes_search_Xtrees = BayesSearchCV(estimator=Xtrees,
                                 search_spaces=param_grid_Xtrees,
                                 n_iter=50,
                                 scoring='r2',
                                 cv=5,
                                 n_points=10,
                                 random_state=28,
                                 n_jobs=-1)
    # Perform BayesSearchCV
    bayes_search_Xtrees.fit(X_train_preprocessed, y_train)
    # Get the best hyperparameters
    best_params = bayes_search_Xtrees.best_params_
    # Get the best model
    best_Xtrees = bayes_search_Xtrees.best_estimator_
    # Calculate feature importances
    importances = best_Xtrees.feature_importances_
    # Get the indices of top features based on feature importances
    indices = np.argsort(importances)[::-1][:10]
    # Get the names of top features based on feature importances
    features_Xtrees = [header_names[i] for i in indices]
    # Store feature importances
    feature_importances['ExtraTrees'] = dict(zip(features_Xtrees, importances))

####################################################################################################

    ##########################
    ### AdaBoost Regressor ###
    ##########################
    
    # Define the hyperparameter grid
    param_grid_Ada = {
        'n_estimators': Integer(50, 500),                         # No. of base estimators
        'learning_rate': Real(0.01, 1.0),                         # Learning rate to shrink each base estimator's contribution
        'loss': Categorical(['linear', 'square', 'exponential'])  # Loss function to update weights
    }
    # Initialize AdaBoostRegressor
    adaboost_model = AdaBoostRegressor(random_state=28)
    # Initialize BayesSearchCV
    bayes_search_Ada = BayesSearchCV(estimator=adaboost_model,
                                     search_spaces=param_grid_Ada,
                                     n_iter=50,
                                     scoring='r2',
                                     cv=5,
                                     n_points=10,
                                     random_state=28,
                                     n_jobs=-1)
    
    # Perform BayesSearchCV
    bayes_search_Ada.fit(X_train_preprocessed, y_train)
    # Get the best hyperparameters
    best_params = bayes_search_Ada.best_params_
    # Get the best model
    best_Ada = bayes_search_Ada.best_estimator_
    # Calculate feature importances
    importances = best_Ada.feature_importances_
    # Get the indices of top features based on feature importances
    indices = np.argsort(importances)[::-1][:10]
    # Get the names of top features based on feature importances
    features_Ada = [header_names[i] for i in indices]
    # Store feature importances
    feature_importances['AdaBoost'] = dict(zip(features_Ada, importances))

####################################################################################################

    #########################
    ### XGBoost Regressor ###
    #########################
    
    # Define the hyperparameter search space
    param_grid_XGB = {
        'n_estimators': Integer(100, 500),                    # No. of trees in the forest
        'learning_rate': Real(0.01, 0.3, prior='uniform'),    # Learning rate
        'max_depth': Categorical([3, 10]),                    # Max depth of each tree
        'min_child_weight': Integer(1, 10),                   # Min sum of instance weight needed in a child
        'subsample': Real(0.6, 1.0, prior='uniform'),         # Subsample ratio of the training instance
        'colsample_bytree': Real(0.6, 1.0, prior='uniform'),  # Subsample ratio of columns when constructing each tree
        'gamma': Real(0, 0.5, prior='uniform'),               # Min loss reduction to further partition on a leaf node
        'reg_alpha': Real(0, 1.0, prior='uniform'),           # L1 reg term on weights
        'reg_lambda': Real(0, 1.0, prior='uniform')           # L2 reg term on weights
    }
    # Initialize XGBRegressor
    xgb = XGBRegressor(random_state=28)

    # Initialize BayesSearchCV
    bayes_search_XGB = BayesSearchCV(estimator=xgb,
                                     search_spaces=param_grid_XGB,
                                     n_iter=50,
                                     scoring='r2',
                                     cv=5,
                                     n_points=10,
                                     random_state=28,
                                     n_jobs=-1)
    
    # Perform BayesSearchCV
    bayes_search_XGB.fit(X_train_preprocessed, y_train)
    # Get the best hyperparameters
    best_params = bayes_search_XGB.best_params_
    # Get the best model
    best_XGB = bayes_search_XGB.best_estimator_
    # Calculate feature importances
    importances = best_XGB.feature_importances_
    # Get the indices of top features based on feature importances
    indices = np.argsort(importances)[::-1][:10]
    # Get the names of top features based on feature importances
    features_XGB = [header_names[i] for i in indices]
    # Store feature importances
    feature_importances['XGB'] = dict(zip(features_XGB, importances))

####################################################################################################

    X_train = X_train_preprocessed[:, indices]
    X_test = X_test_preprocessed[:, indices]

    return (features_rf,
            features_Dtree,
            features_pca, 
            features_rfecv, 
            features_gbm,
            features_svr, 
            features_Xtrees,
            features_Ada,
            features_XGB,
            feature_importances)