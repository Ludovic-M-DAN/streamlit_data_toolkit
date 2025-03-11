import pandas as pd

def load_data(file_path, separator=','):
    """
    Charge un fichier CSV ou Excel dans un DataFrame pandas.
    
    :param file_path: Chemin ou objet fichier à charger
    :param separator: Séparateur pour les fichiers CSV (par défaut ',')
    :return: DataFrame pandas
    """
    if file_path.name.endswith('.csv'):
        return pd.read_csv(file_path, sep=separator)
    elif file_path.name.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Format de fichier non supporté. Veuillez utiliser CSV ou Excel.")

def sample_data(df, method, n=None, frac=None):
    """
    Échantillonne le DataFrame selon la méthode spécifiée.
    
    :param df: DataFrame à échantillonner
    :param method: Méthode d'échantillonnage ('random_total', 'random_representatif', 'first_n', 'last_n')
    :param n: Nombre de lignes à échantillonner (si applicable)
    :param frac: Fraction de lignes à échantillonner (si applicable)
    :return: DataFrame échantillonné
    """
    if method == 'random_total':
        return df.sample(n=n) if n else df.sample(frac=frac)
    elif method == 'random_representatif':
        # Échantillonnage aléatoire simple (à améliorer avec stratification si besoin)
        return df.sample(n=n) if n else df.sample(frac=frac)
    elif method == 'first_n':
        return df.head(n)
    elif method == 'last_n':
        return df.tail(n)
    else:
        raise ValueError("Méthode d'échantillonnage non supportée.")