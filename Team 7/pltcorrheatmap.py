import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_corr_heatmap(corr_matrix, selected_feature_names, threshold=0.65):
    selected_indices = [corr_matrix.columns.get_loc(col) for col in selected_feature_names]
    corr_matrix_selected = corr_matrix.iloc[selected_indices, selected_indices]

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr_matrix_selected, dtype=bool))

    # Plot heatmap
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr_matrix_selected, annot=True, mask=mask, cmap='coolwarm', fmt=".2f", linewidths=0.5)

    # Add labels only for correlations greater than the threshold and below the diagonal
    for i in range(len(corr_matrix_selected.columns)):
        for j in range(i):
            if corr_matrix_selected.iloc[i, j] > threshold:
                plt.text(j + 0.5, i + 0.5, f"{corr_matrix_selected.iloc[i, j]:.2f}", ha='center', va='center', color='black')

    plt.title('Correlation Heatmap')
    plt.show()
