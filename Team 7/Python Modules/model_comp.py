import numpy as np
import matplotlib.pyplot as plt

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
    axs[0].set_ylim(0.4, 0.8)

    axs[1].bar(model_names, MSE_s, color=mse_colors)
    axs[1].set_xlabel('Model', fontdict={'fontsize': 10, 'fontweight': 'bold'})
    axs[1].set_ylabel('MSE', fontdict={'fontsize': 10, 'fontweight': 'bold'})
    axs[1].set_title('Model MSE Values', fontdict={'fontsize': 12, 'fontweight': 'bold'})
    axs[1].tick_params(axis='x', rotation=0)
    axs[1].set_ylim(0.0005, 0.0025)

    plt.tight_layout()
    plt.show()