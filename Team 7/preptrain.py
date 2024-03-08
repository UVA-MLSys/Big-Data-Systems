import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.svm import SVR

def preprocess_and_train(df, df_last, labels):
    """
    Preprocesses the data and trains a Support Vector Regression (SVR) model.
    
    Parameters:
    -----------
    df : pandas DataFrame
        The input training data containing features.
        
    df_last : pandas DataFrame
        The input test data to be predicted by the trained model.
        
    labels : array-like
        The target labels corresponding to the training data.

    Returns:
    --------
    selected_feature_names : list
        List of selected feature names after feature selection.
        
    X_train : array-like
        Preprocessed training features selected based on the feature selection process.
        
    X_test : array-like
        Preprocessed test features selected based on the feature selection process.
        
    y_train : array-like
        Labels corresponding to the preprocessed training data.
        
    y_test : array-like
        Labels corresponding to the preprocessed test data.
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

    header_names = [col.split("__")[1] for col in preprocessor.get_feature_names_out()]

    # Define SVR regressor
    regressor = SVR(kernel="linear")

    # Combine preprocessing and regressor into one pipeline
    pipeline = Pipeline(steps=[
        ('feature_selection', SelectKBest(score_func=f_regression, k=10)),  
        ('regressor', regressor)
    ])

    # Fit the pipeline on training data
    pipeline.fit(X_train_preprocessed, y_train)

    # Get selected feature indices
    selected_indices = pipeline.named_steps['feature_selection'].get_support(indices=True)

    # Extract feature names
    selected_feature_names = [header_names[i] for i in selected_indices]

    # Filter training and testing data to include only selected features
    X_train = X_train_preprocessed[:, selected_indices]
    X_test = X_test_preprocessed[:, selected_indices]

    # Transform df_last to include only selected features
    df_last_selected = pd.DataFrame(df_last_preprocessed, columns=header_names)
    df_last_selected = df_last_selected[selected_feature_names]

    return selected_feature_names, X_train, X_test, y_train, y_test