# **Introduction**

## **Project Goal**:

Historically, there have been several metrics that data scientists and analysts have developed and used to determine how valuable a given player is to their team's success. Some examples are VORP, Box-Plus-Minus, and Win Shares, amongst others. We aim to develop a formula/equation that weights each of these parameters based on how well they predict MVP rankings, then apply it to untrained years to see if our developed "MVP index" can correctly predict the MVP rankings in those years. We can tinker with the formula as we see fit based on what we believe is vital to a player's value and compare it to other methods developed by reputable analyst companies (i.e., the RAPTOR metric developed by FiveThirtyEight)

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
