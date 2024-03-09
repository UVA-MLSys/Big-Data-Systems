from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression, SelectFromModel, RFE, RFECV, mutual_info_regression
from sklearn.cluster import FeatureAgglomeration
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn import metrics, linear_model
from sklearn.linear_model import LinearRegression
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
    - Embedded Method 2: Support Vector Regressor (RBF Kernel).
    - PCA: Principal Component Analysis.
    - Stability Selection: Lasso-based method for feature selection.
    - RFECV: Recursive Feature Elimination with Cross-Validation.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Input data to be preprocessed and trained on.
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
        - features_stability_selection : list
            Selected features using Stability Selection with Lasso.
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

    # Extract feature names without prepending "num__" or "cat__"
    header_names = [col.split("__")[1] if "__" in col else col for col in preprocessor.get_feature_names_out()]

    # Feature selection

    # Filter Method - SelectKBest using ANOVA F-value
    selector_filter = SelectKBest(score_func=f_regression, k=10)
    selector_filter.fit(X_train_preprocessed, y_train)
    selected_indices_filter = selector_filter.get_support(indices=True)
    features_filter = [header_names[i] for i in selected_indices_filter]

    # Wrapper Method - Random Forest Feature Importance
    rf = RandomForestRegressor(n_estimators=100, random_state=28)
    rf.fit(X_train_preprocessed, y_train)
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    features_wrapper_indices = indices[:10]
    features_wrapper = [header_names[i] for i in features_wrapper_indices]

    # Embedded Method - L1-based feature selection using Lasso
    lasso = LassoCV(cv=5, random_state=28, max_iter=10000, alphas=[0.01, 0.1, 1.0, 10.0])
    lasso.fit(X_train_preprocessed, y_train)
    mask = lasso.coef_ != 0
    features_embedded_indices = [i for i, m in enumerate(mask) if m]
    features_embedded = [header_names[i] for i in features_embedded_indices]

    # PCA
    pca = PCA(n_components=10)
    pca.fit(X_train_preprocessed)
    X_train_pca = pca.transform(X_train_preprocessed)
    features_pca_indices = np.argsort(np.abs(pca.components_), axis=1)[:, -10:]
    features_pca = []
    
    # Get the original feature names corresponding to selected principal components
    for i, component_indices in enumerate(features_pca_indices):
        original_features = [header_names[idx] for idx in component_indices]
        features_pca.append(original_features)

    # Stability Selection with Lasso
    stable_lasso = LassoCV(cv=5, random_state=28, max_iter=10000, alphas=[0.01, 0.1, 1.0, 10.0])
    sfm = SelectFromModel(estimator=stable_lasso)
    sfm.fit(X_train_preprocessed, y_train)
    features_stability_selection_indices = sfm.get_support(indices=True)
    features_stability_selection = [header_names[i] for i in features_stability_selection_indices]

    # RFECV
    estimator_rfecv = GradientBoostingRegressor(n_estimators=100, random_state=28)
    selector_rfecv = RFECV(estimator_rfecv, step=1, cv=10)
    selector_rfecv.fit(X_train_preprocessed, y_train)
    selected_indices_rfecv = selector_rfecv.get_support(indices=True)
    features_rfecv_indices = np.argsort(selector_rfecv.cv_results_['mean_test_score'])[::-1][:10]
    features_rfecv = [header_names[i] for i in features_rfecv_indices]

    # Wrapper Method - GBM Feature Importance
    gbm = GradientBoostingRegressor(n_estimators=100, random_state=28)
    gbm.fit(X_train_preprocessed, y_train)
    importances_gbm = gbm.feature_importances_
    indices_gbm = np.argsort(importances_gbm)[::-1]
    features_wrapper_indices_gbm = indices_gbm[:10]
    features_wrapper_gbm = [header_names[i] for i in features_wrapper_indices_gbm]

    # Embedded Method - Support Vector Regressor
    svr = SVR(kernel='rbf')
    svr.fit(X_train_preprocessed, y_train)
    perm_importance = permutation_importance(svr, X_train_preprocessed, y_train, n_repeats=10, random_state=28)
    features_embedded_svr_indices = np.argsort(perm_importance.importances_mean)[::-1][:10]
    features_embedded_svr = [header_names[i] for i in features_embedded_svr_indices]

    # Choose the selected features based on the method with the highest performance
    # For now, let's just return the selected features from the Wrapper Method
    feature_names = features_wrapper
    X_train = X_train_preprocessed[:, features_wrapper_indices]
    X_test = X_test_preprocessed[:, features_wrapper_indices]

    return (features_filter, features_wrapper, 
            features_embedded, features_pca,
            features_stability_selection, feature_names,
            features_rfecv, features_wrapper_gbm,
            features_embedded_svr,
            X_train, X_test, y_train, y_test)