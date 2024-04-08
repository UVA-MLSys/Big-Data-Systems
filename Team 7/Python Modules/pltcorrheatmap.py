import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap

def plot_corr_heatmap(corr_matrix, selected_feature_names, threshold=0.65, width=7, height=4):
    """
    Plot a correlation heatmap for selected features.

    Parameters:
    -----------
    corr_matrix : pandas.DataFrame
        DataFrame containing the correlation matrix.

    selected_feature_names : list
        List of selected feature names for which the heatmap is to be plotted.

    threshold : float, optional (default=0.65)
        Threshold value to highlight correlations greater than or equal to this value.

    width : int, optional (default=7)
        Width of the heatmap figure.

    height : int, optional (default=4)
        Height of the heatmap figure.

    Returns:
    --------
    None
        This function only displays the heatmap plot.
    """
    selected_indices = [corr_matrix.columns.get_loc(col) for col in selected_feature_names]
    corr_matrix_selected = corr_matrix.iloc[selected_indices, selected_indices]
    
    # Set style to seaborn-poster
    plt.style.use('fivethirtyeight')
    
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr_matrix_selected, dtype=bool))
    
    # Custom colormap
    custom_cmap = ListedColormap(['#232D4B', '#6f7890', '#9ea3b0', '#C8CBD2', 
                                  '#F9DCBF', '#f4c18f', '#f29c46', '#de6e00'])
    
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(width, height))
    
    # Plot heatmap
    sns.heatmap(corr_matrix_selected, annot=False, mask=mask, cmap=custom_cmap, linewidths=0.3)
    
    # Add labels for correlations greater than or equal to the threshold and below the diagonal
    for i in range(len(corr_matrix_selected.columns)):
        for j in range(i):
            if abs(corr_matrix_selected.iloc[i, j]) >= threshold:
                ax.text(j + 0.5, i + 0.5, f"{corr_matrix_selected.iloc[i, j]:.2f}", ha='center', va='center', color='black')
    
    plt.title('Correlation Heatmap')
    plt.show()