import platform
import multiprocessing
import os
from tabulate import tabulate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap

"""
helper_functions.py

This module contains various helper functions for system information retrieval, model evaluation, and visualization.

Functions:
1. get_hardware_details():
   Retrieve basic hardware details of the system.

2. print_importances(features, model):
   Print the feature importances of a model.

3. print_dict_imps(feature_importances):
   Print the feature importances in a visually appealing table format side-by-side.

4. avg_imps(feature_importances):
   Calculate the average feature importances across different methods.

5. create_imp_df(model_names, models, feature_names):
   Create a DataFrame of feature importances for each model.

6. plot_corr_heatmap(corr_matrix, selected_feature_names, threshold=0.65, width=7, height=4):
   Plot a correlation heatmap for selected features.

7. plot_model_performance(model_names, r_sqs, MSE_s):
   Plot the R-squared and MSE values of different regression models.
"""

def get_hardware_details():
    """
    Retrieve basic hardware details of the system.

    Returns:
    dict: A dictionary containing the following hardware details:
        - 'System': The name of the operating system.
        - 'Node Name': The name of the node (typically the hostname).
        - 'Release': The operating system release.
        - 'Version': The operating system version.
        - 'Machine': The machine hardware name.
        - 'Processor': The processor type.
        - 'CPU Cores': The number of CPU cores.
        - 'CPU Vendor': The CPU vendor information.
        - 'CPU Model': The CPU model information.
        - 'RAM': The amount of RAM allocated to the job in gigabytes (if applicable).
    """
    details = {}
    
    details['System'] = platform.system()
    details['Node Name'] = platform.node()
    details['Release'] = platform.release()
    details['Version'] = platform.version()
    details['Machine'] = platform.machine()
    details['Processor'] = platform.processor()
    
    # Get number of CPU cores
    details['CPU Cores'] = len(os.sched_getaffinity(0))
    
    # Get CPU vendor and model
    cpu_info = {}
    with open('/proc/cpuinfo', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                key = parts[0].strip()
                value = parts[1].strip()
                cpu_info[key] = value
    details['CPU Vendor'] = cpu_info.get('vendor_id', 'N/A')
    details['CPU Model'] = cpu_info.get('model name', 'N/A')
    
    # Get amount of RAM allocated for the job (if applicable)
    allocated_ram_gb = None
    if 'SLURM_MEM_PER_NODE' in os.environ:
        slurm_mem_per_node = os.environ['SLURM_MEM_PER_NODE']
        allocated_ram_mb = int(slurm_mem_per_node.strip().split()[0])
        allocated_ram_gb = allocated_ram_mb / 1024.0  # Convert to gigabytes
    elif 'PBS_NUM_PPN' in os.environ:
        # Example for PBS/Torque, you may need to adjust based on your system
        num_ppn = int(os.environ['PBS_NUM_PPN'])
        total_ram_mb = psutil.virtual_memory().total / (1024.0 ** 2)  # Convert to megabytes
        allocated_ram_gb = total_ram_mb / num_ppn  # Divide by number of processes per node
    details['RAM'] = allocated_ram_gb
    
    return details

def print_importances(features, model):
    """
    Print the feature importances of a model.

    Parameters
    ----------
    features : list
        List of feature names.
    model : object
        Fitted model object with a 'feature_importances_' attribute.

    Returns
    -------
    None
    """
    feature_dict = dict(zip(features, model.feature_importances_))
    sorted_dict = sorted(feature_dict.items(), key=lambda x: x[1], reverse=True)
    print("Feature Importances:")
    for i, (feature, imp) in enumerate(sorted_dict, 1):
        print(f"{i}: {feature} : {imp:.5f}")
        
def print_dict_imps(feature_importances):
    """
    Print the feature importances in a visually appealing table format side-by-side.

    Parameters
    ----------
    feature_importances : dict
        Dictionary containing feature importances with method names as keys.

    Returns
    -------
    None
    """
    tables = []
    for method, importances in feature_importances.items():
        sorted_importances = sorted(importances.items(), key=lambda x: x[1], reverse=True)
        # Round the importances to 5 decimal places
        rounded_importances = [(feature, round(imp, 5)) for feature, imp in sorted_importances]
        # Construct the table with headers and rounded importances
        table = tabulate(rounded_importances, headers=["Feature", "Importance"], tablefmt="fancy_grid", showindex=False)
        tables.append((method, table))

    # Split tables into groups of four
    grouped_tables = [tables[i:i+4] for i in range(0, len(tables), 4)]

    # Print tables in rows of four
    for group in grouped_tables:
        max_rows = max(len(table.split('\n')) for _, table in group)
        table_strings = []
        for method, table in group:
            table_lines = table.split('\n')
            # Pad with empty lines if necessary
            table_lines += [''] * (max_rows - len(table_lines))
            # Insert method name in the first row
            table_lines[0] = f"{method:^{len(table_lines[0])}}"
            table_strings.append('\n'.join(table_lines))
        combined_table = '\n'.join('  '.join(lines) for lines in zip(*[table.split('\n') for table in table_strings]))
        print(combined_table)
        print()
    
def avg_imps(feature_importances):
    """
    Calculate the average feature importances across different methods.

    Parameters
    ----------
    feature_importances : dict
        Dictionary containing feature importances for different methods.

    Returns
    -------
    dict
        Dictionary containing the average feature importances across different methods.
    """
    average_importances = {}
    total_occurrences = {}

    # Iterate over each feature
    for method, imp_dict in feature_importances.items():
        for feature, importance in imp_dict.items():
            # If the feature is not in average_importances, initialize it with the importance
            if feature not in average_importances:
                average_importances[feature] = 0
                total_occurrences[feature] = 0
            average_importances[feature] += importance
            total_occurrences[feature] += 1

    # Calculate the average importance for each feature
    for feature in average_importances:
        average_importances[feature] /= total_occurrences[feature]

    # Sort the average importances dictionary by importance values in descending order
    sorted_imps = dict(sorted(average_importances.items(), key=lambda item: item[1], reverse=True))

    # Print the sorted average importances for each feature and store the top ten features
    top_features = []
    for i, (feature, importance) in enumerate(sorted_imps.items(), start=1):
        print(f"{i}. {feature}: {importance:.5f}")
        if i <= 10:
            top_features.append(feature)

    print("Top 10 Features:", top_features)

    return average_importances


def create_imp_df(model_names, models, feature_names):
    """
    Create a DataFrame of feature importances for each model.

    Args:
    - model_names (list): List of model names.
    - models (list): List of model objects.
    - feature_names (list): List of feature names.

    Returns:
    - df_imps (DataFrame): DataFrame of feature importances.
    """
    # Create an empty dictionary to store feature importances
    feature_importances_dict = {}

    # Iterate over each model
    for model_name, model in zip(model_names, models):
        # Get feature importances for the current model
        importances = model.feature_importances_

        # Create a dictionary for the current model
        model_dict = {
            feature: importance for feature, importance in zip(feature_names, importances)
        }

        # Add the model dictionary to the feature importances dictionary
        feature_importances_dict[model_name] = model_dict

    # Create DataFrame from dictionary and transpose it
    df_imps = pd.DataFrame(feature_importances_dict).T
    return df_imps


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
    
    
def plot_model_performance(model_names, r_sqs, MSE_s):
    """
    Plot the R-squared and MSE values of different regression models.

    Parameters:
    -----------
    model_names : list
        A list of model names.
    
    r_sqs : list
        A list of R-squared values corresponding to each model.
        
    MSE_s : list
        A list of MSE values corresponding to each model.
    """
    # Determine colors for R-squared bars
    r_sq_colors = ['#E57200' if r == max(r_sqs) else '#232D4B' for r in r_sqs]

    # Determine colors for MSE bars
    mse_colors = ['#E57200' if mse == min(MSE_s) else '#232D4B' for mse in MSE_s]

    plt.style.use('fivethirtyeight')
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    axs[0].bar(model_names, r_sqs, color=r_sq_colors)
    axs[0].set_xlabel('Model', fontdict={'fontsize': 10, 'fontweight': 'bold'})
    axs[0].set_ylabel('R-squared', fontdict={'fontsize': 10, 'fontweight': 'bold'})
    axs[0].set_title('Model R-squared Values', fontdict={'fontsize': 12, 'fontweight': 'bold'})
    axs[0].tick_params(axis='x', rotation=0)
    axs[0].set_ylim(0.5, 0.8)

    axs[1].bar(model_names, MSE_s, color=mse_colors)
    axs[1].set_xlabel('Model', fontdict={'fontsize': 10, 'fontweight': 'bold'})
    axs[1].set_ylabel('MSE', fontdict={'fontsize': 10, 'fontweight': 'bold'})
    axs[1].set_title('Model MSE Values', fontdict={'fontsize': 12, 'fontweight': 'bold'})
    axs[1].tick_params(axis='x', rotation=0)
    axs[1].set_ylim(0.001, 0.0025)

    plt.tight_layout()
    plt.show()