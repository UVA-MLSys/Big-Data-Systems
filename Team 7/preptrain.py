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
    # Define numeric columns excluding "Pos"
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df, 
                                                        labels, 
                                                        test_size=0.2, 
                                                        shuffle=True, random_state=28)

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
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    # Preprocess df_last
    df_last = preprocessor.transform(df_last)

    header_names = [col.split("__")[1] for col in preprocessor.get_feature_names_out()]

    # Define SVR regressor
    regressor = SVR(kernel="linear")

    # Combine preprocessing and regressor into one pipeline
    pipeline = Pipeline(steps=[
        ('feature_selection', SelectKBest(score_func=f_regression, k=10)),  
        ('regressor', regressor)
    ])

    # Fit the pipeline on training data
    pipeline.fit(X_train, y_train)

    # Evaluate on test data
    accuracy = pipeline.score(X_test, y_test)

    # Get selected feature indices
    selected_indices = pipeline.named_steps['feature_selection'].get_support(indices=True)

    # Extract feature names
    # Extract feature names
    selected_feature_names = [header_names[i] for i in selected_indices]


    # Filter training and testing data to include only selected features
    X_train = X_train[:, selected_indices]
    X_test = X_test[:, selected_indices]

    # Transform df_last to include only selected features
    df_last = pd.DataFrame(df_last, columns=header_names)
    df_last = df_last[selected_feature_names]

    return selected_feature_names, X_train, X_test, y_train, y_test