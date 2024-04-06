from skopt import BayesSearchCV
from skopt.space import Categorical, Real, Integer
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression, SelectFromModel, RFE, RFECV, mutual_info_regression
from sklearn.cluster import FeatureAgglomeration
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn import metrics, linear_model
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor
from scipy.stats import randint
from sklearn.svm import SVR
from sklearn.inspection import permutation_importance
import warnings
from sklearn.exceptions import ConvergenceWarning
import pandas as pd
import numpy as np


def preprocess_and_train(df, df_last, labels):
    """
    Preprocesses the data and selects features using various feature selection methods, including:

    Feature Selection Methods:
    ---------------------------
    - Filter Method: SelectKBest using ANOVA F-value.
    - Wrapper Method 1: Random Forest Feature Importance.
    - Wrapper Method 2: Gradient Boosting Machine Feature Importance.
    - Embedded Method: L1-based feature selection using Lasso.
    - Embedded Method 2: Support Vector Regressor.
    - PCA: Principal Component Analysis.
    - RFECV: Recursive Feature Elimination with Cross-Validation.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Input data.
    df_last : pandas DataFrame
        Dataframe for the last iteration, used for preprocessing consistency.
    labels : array-like
        Target labels.
        
    Returns:
    --------
    tuple
        A tuple containing selected features and preprocessed data for training and testing:
        - features_filter : list
            Selected features using Filter Method (ANOVA F-value).
        - features_wrapper : list
            Selected features using Wrapper Method (Random Forest Feature Importance).
        - features_embedded : list
            Selected features using Embedded Method (L1-based feature selection with Lasso).
        - features_pca : list
            Selected features using PCA.
        - feature_names : list
            Names of selected features based on the method with the highest performance (Wrapper Method for now).
        - features_rfecv : list
            Selected features using Recursive Feature Elimination with Cross-Validation (RFECV).
        - features_wrapper_gbm : list
            Selected features using Wrapper Method (Gradient Boosting Machine Feature Importance).
        - features_embedded_svr : list
            Selected features using Embedded Method (Support Vector Regressor).
        - X_train : numpy array
            Preprocessed training data.
        - X_test : numpy array
            Preprocessed testing data.
        - y_train : array-like
            Target labels for training data.
        - y_test : array-like
            Target labels for testing data.
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

####################################################################################################
                                        #########################
                                        ### Feature selection ###
                                        #########################
####################################################################################################
    
    #######################################
    ### SelectKBest using ANOVA F-value ###
    #######################################
    selector_filter = SelectKBest(score_func=f_regression, k=10)
    selector_filter.fit(X_train_preprocessed, y_train)
    selected_indices_filter = selector_filter.get_support(indices=True)
    features_filter = [header_names[i] for i in selected_indices_filter]

####################################################################################################

    ########################################
    ### Random Forest Feature Importance ###
    ########################################
    
    # Define the hyperparameter grid
    param_grid_rf = {
        'n_estimators': Integer(200, 300),              # No. of trees in the forest
        'max_features': Categorical(['log2', 'sqrt']),  # No. of features to consider at every split
        'max_depth': Categorical([None, 10, 20]),       # Max depth of the trees
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
                                    n_points=7,
                                    random_state=28, 
                                    n_jobs=-1)
    
    # Perform BayesSearchCV
    bayes_search_rf.fit(X_train_preprocessed, y_train)
    # Get the best hyperparameters
    best_params_rf = bayes_search_rf.best_params_
    # Get the best model
    best_rf_model = bayes_search_rf.best_estimator_
    # Calculate feature importances
    importances = best_rf_model.feature_importances_
    # Get the indices of top features based on feature importances
    indices = np.argsort(importances)[::-1][:10]
    # Get the names of top features based on feature importances
    features_wrapper = [header_names[i] for i in indices]
####################################################################################################

    ##############################################
    ### L1-based feature selection using Lasso ###
    ##############################################
    lasso = LassoCV(cv=5, random_state=28, max_iter=1000, alphas=[0.01, 0.1], n_jobs=-1)
    lasso.fit(X_train_preprocessed, y_train)
    mask = lasso.coef_ != 0
    features_embedded_indices = [i for i, m in enumerate(mask) if m]
    features_embedded = [header_names[i] for i in features_embedded_indices]

####################################################################################################

    ###########
    ### PCA ###
    ###########
    pca = PCA(n_components=10)
    pca.fit(X_train_preprocessed)
    X_train_pca = pca.transform(X_train_preprocessed)
    features_pca_indices = np.argsort(np.abs(pca.components_), axis=1)[:, -10:]
    features_pca = []
    # Get the original feature names corresponding to selected principal components
    for i, component_indices in enumerate(features_pca_indices):
        original_features = [header_names[idx] for idx in component_indices]
        features_pca.append(original_features)

####################################################################################################

    #############
    ### RFECV ###
    #############

    # Define the hyperparameter grid
    param_grid_gb = {
        'n_estimators': Integer(100, 300),                  # No. of boosting stages
        'learning_rate': Real(0.05, 0.1, prior='uniform'),  # Learning rate
        'max_depth': Integer(3, 5),                         # Max depth of individual trees
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
                                    n_points=7,
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

    ##############################
    ### GBM Feature Importance ###
    ##############################

    # Define the parameter grid for GradientBoostingRegressor
    # Define the hyperparameter grid
    param_grid_gb = {
        'n_estimators': Integer(100, 300),                  # No. of boosting stages
        'learning_rate': Real(0.05, 0.1, prior='uniform'),  # Learning rate
        'max_depth': Integer(3, 5),                         # Max depth of the individual trees
        'min_samples_split': Integer(2, 5),                 # Min no. of samples required to split an internal node
        'min_samples_leaf': Integer(1, 2),                  # Min no. of samples required to be at a leaf node
        'subsample': Real(0.6, 0.8, prior='uniform'),       # Fraction of samples used to fit individual base learners
        'max_features': Categorical(['log2', 'sqrt'])       # No. of features to consider when looking for the best split
    }
    
    # Create the GradientBoostingRegressor estimator
    gbm = GradientBoostingRegressor()
    # Create the BayesSearchCV object for GradientBoostingRegressor
    bayes_search_gb = BayesSearchCV(estimator=gbm, 
                                    search_spaces=param_grid_gb, 
                                    n_iter=50, 
                                    scoring='r2', 
                                    cv=5,
                                    n_points=7,
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
    features_wrapper_gbm = [header_names[i] for i in indices_gbm]

####################################################################################################

    ################################
    ### Support Vector Regressor ###
    ################################

    # Define the parameter grid for SVR
    param_grid_svr = {
        'kernel': Categorical(['linear', 'rbf', 'poly']),  # Vary the kernel types
        'C': Real(0.1, 1.0, prior='uniform'),              # Vary the regularization parame
        'gamma': Categorical(['scale', 'auto'])            # Vary the gamma parame
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
                                         n_points=7,
                                         n_jobs=-1, 
                                         verbose=False)
        # Fit the BayesSearchCV to the preprocessed training data
        bayes_search_svr.fit(X_train_preprocessed, y_train)
    
    # Get the best SVR estimator from the BayesSearchCV
    best_svr_estimator = bayes_search_svr.best_estimator_
    # Calculate permutation importance using the best SVR estimator
    perm_importance = permutation_importance(best_svr_estimator, X_train_preprocessed, y_train, n_repeats=3, random_state=28)
    # Get the indices of top features based on permutation importance
    features_embedded_svr_indices = np.argsort(perm_importance.importances_mean)[::-1][:10]
    # Get the names of top features based on permutation importance
    features_embedded_svr = [header_names[i] for i in features_embedded_svr_indices]

####################################################################################################

    # Choose the selected features based on the method with the highest performance
    # For now, let's just return the selected features from the Wrapper Method
    feature_names = features_wrapper
    X_train = X_train_preprocessed[:, indices]
    X_test = X_test_preprocessed[:, indices]

    return (features_filter, features_wrapper, 
            features_embedded, features_pca,
            feature_names,features_rfecv, 
            features_wrapper_gbm,features_embedded_svr,
            X_train, X_test, y_train, y_test)