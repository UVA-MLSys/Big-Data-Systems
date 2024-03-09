# **Introduction**

## **Project Goal**:
Data Scientists and analysts have developed several metrics for determining a player's value to their team's success. Prominent examples include Value Over Replacement Player (VORP), Box Plus/Minus (BPM), and FiveThirtyEight's Robust Algorithm (using) Player Tracking (and) On/Off Ratings (RAPTOR)​. We aim to develop a multivariate index that weighs these parameters based on how well they predict MVP rankings, then test it on unseen data for the most recent five seasons to see if our "MVP index" correctly predicts the MVP rankings.​ We will experiment with the index formula and compare it to other methods developed by reputable analyst sources.

## **Manifest**:

### **Jupyter Notebooks**:

#### FeatureSelection.ipynb:

Feature Selection notebook where we use the `preprocess_and_train` function from `preptrain.py` and ensemble the methods to generate the best 10 features.
  
#### DataCleaning_EDA.ipynb:
  
Exploratory notebook where the data is cleaned; includes some basic EDA.

#### Models.ipynb:

Modeling notebook where we use the selected features (from `df_selected.csv`) to train and evaluate a range of models and extract their feature importance. These results will inform how we weight features in the index.

### **Data Files**:

#### df_clean.csv:
  
Main .csv file used for training and validation.

#### df_last.csv:
  
Testing .csv file for examining model performance on last 5 seasons (2018-22).

#### df_selected.csv:

Selected features .csv containing the subset of predictor variables.

### **Python Module Files (helper functions, classes)**

#### pltcorrheatmap.py:
  
Custom function for generating correlation heat maps as we determine feature importance.

#### preptrain.py:
  
Custom function/pipeline for preprocessing and feature selection, described below:

- Defining Numeric Columns (Excluding "Pos"):

This step identifies the numeric columns in the input DataFrame `df`, excluding the column labeled "Pos" for player position.

- Splitting Data into Training and Testing Sets:

Splits the input data into training and testing sets using the `train_test_split` function from `scikit-learn`.

- Defining Preprocessing Steps:

Defines the preprocessing steps using pipelines. For numeric features, we impute missing values with the median value and then scale the features using standardization (subtracting the mean and dividing by the standard deviation). For categorical features (specifically "Pos"), we apply one-hot encoding while ignoring unknown categories.

- Preprocessing Training and Testing Data:

Applies the preprocessing separately to the training and testing datasets using the `fit_transform` and `transform` methods of the `ColumnTransformer`.

- Extracting Feature Names:

Extracts the feature names from the `ColumnTransformer` object. This step removes any prefixes such as "num__" or "cat__".

- Filter Method - SelectKBest:

Uses SelectKBest with ANOVA F-value to select the top 10 features based on their scores. These scores represent the strength of the relationship between each feature and the target variable.

- Wrapper Method 1 - Random Forest Feature Importance:

Trains a Random Forest Regressor on the preprocessed training data to determine feature importance and selects the top 10 features with the highest feature importance scores.

- Embedded Method - L1-based feature selection using Lasso:

LassoCV (Lasso Cross-validation) is employed to perform L1-based feature selection. It iteratively fits Lasso models with different regularization strengths (alphas) and selects features based on non-zero coefficients.

- Performs Principal Component Analysis (PCA):

Performs PCA to reduce the dimensionality of the data and select the top 10 principal components as features.

- Stability Selection with Lasso:
Uses Stability Selection with Lasso to select features. We apply LassoCV within SelectFromModel to select features based on stability across multiple Lasso models.

- Recursive Feature Elimination with Cross-Validation (RFECV):

Applies RFECV, a wrapper method that recursively selects features by recursively training the model and selecting the best-performing subset of features through cross-validation.

- Wrapper Method 2 - Gradient Boosting Machine Feature Importance

Trains a Gradient Boosting Machine model on the preprocessed training data to determine feature importance and selects the top 10 features with the highest feature importance scores.

- Embedded Method 2 - Support Vector Regressor

Uses Support Vector Regressor (SVR) within SelectFromModel to perform embedded feature selection. Features are selected based on the coefficients obtained from the SVR model.

- Preparing Final Data for Training:

Extracts the selected features from the preprocessed training and testing data and prepares the final datasets (X_train, X_test, y_train, y_test) for model training and evaluation.

- Returning Results:

The function returns various components: the selected features from each method (features_filter, features_wrapper, features_embedded), the names of the selected features (feature_names), and the preprocessed training and testing data along with their corresponding labels.
