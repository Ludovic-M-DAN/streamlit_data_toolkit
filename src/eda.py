import pandas as pd

def get_data_info(df):
    """
    Génère un dictionnaire avec les informations de base sur le DataFrame.
    
    :param df: DataFrame à analyser
    :return: Dictionnaire avec les informations
    """
    info = {
        'dimensions': df.shape,
        'column_names': df.columns.tolist(),
        'data_types': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict()
    }
    return info