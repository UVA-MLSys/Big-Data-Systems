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
    print(f"Feature Importances:")
    for feature, imp in sorted_dict:
        print(feature, ":", imp)