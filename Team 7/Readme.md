# **Introduction**

## **Project Goal**:
Data Scientists and analysts have developed several metrics for determining a player's value to their team's success. Prominent examples include Value Over Replacement Player (VORP), Box Plus/Minus (BPM), and FiveThirtyEight's Robust Algorithm (using) Player Tracking (and) On/Off Ratings (RAPTOR)​. We aim to develop a multivariate index that weighs these parameters based on how well they predict MVP rankings, then test it on unseen data for the most recent five seasons to see if our "MVP index" correctly predicts the MVP rankings.​ We will experiment with the index formula and compare it to other methods developed by reputable analyst sources.

## **Manifest**:

### **Jupyter Notebooks**:

`FeatureSelection_Modeling.ipynb`:

Feature Selection and basic modeling notebook.
  
`MVP.ipynb`:
  
Exploratory notebook where the data is cleaned; includes some basic EDA.

### **Data Files**:

`df_clean.csv`:
  
Main .csv file used for training and validation.

`df_last.csv`:
  
Testing .csv file for examining model performance on last 5 seasons (2018-22).

### **Python Module Files (helper functions, classes)**

`pltcorrheatmap.py`:
  
Custom function for generating correlation heat maps as we determine feature importance.

`preptrain.py`:
  
Custom function/pipeline for preprocessing.
