# treatments.py
import pandas as pd

def rename_columns(df, new_names):
    """
    Renomme les colonnes d'un DataFrame selon le dictionnaire fourni.
    
    :param df: DataFrame original
    :param new_names: Dictionnaire de mapping {ancien_nom: nouveau_nom}
    :return: DataFrame avec les colonnes renommées
    """
    return df.rename(columns=new_names)

def fill_missing_values(df, columns, method, custom_value=None):
    """
    Remplit les valeurs nulles dans les colonnes sélectionnées avec la méthode choisie.
    
    :param df: DataFrame original
    :param columns: Liste des colonnes à traiter
    :param method: Méthode de remplissage. Options : "0", "mean", "median", "ffill", "bfill", "custom"
    :param custom_value: Valeur personnalisée à utiliser si method == "custom"
    :return: DataFrame modifié avec les valeurs nulles remplies
    """
    df_filled = df.copy()
    for col in columns:
        if method == "0":
            df_filled[col] = df_filled[col].fillna(0)
        elif method == "mean":
            df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
        elif method == "median":
            df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        elif method == "ffill":
            df_filled[col] = df_filled[col].fillna(method="ffill")
        elif method == "bfill":
            df_filled[col] = df_filled[col].fillna(method="bfill")
        elif method == "custom":
            df_filled[col] = df_filled[col].fillna(custom_value)
    return df_filled
