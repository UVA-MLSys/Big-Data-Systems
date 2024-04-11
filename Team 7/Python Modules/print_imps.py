from tabulate import tabulate
import pandas as pd

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