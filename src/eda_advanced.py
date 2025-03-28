# eda_advanced.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def descriptive_stats(df):
    """Renvoie les statistiques descriptives pour le DataFrame."""
    return df.describe()

def plot_distribution(df, col):
    """Génère un histogramme avec courbe de densité pour la colonne spécifiée."""
    fig, ax = plt.subplots()
    sns.histplot(df[col], kde=True, ax=ax)
    return fig

def plot_correlation(df):
    """
    Génère une matrice de corrélation pour les colonnes numériques 
    si au moins deux sont présentes.
    """
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numerical_cols) > 1:
        corr = df[numerical_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        return fig
    return None

def plot_missing_values(df):
    """
    Visualise les valeurs manquantes sous forme de barres.
    """
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        fig, ax = plt.subplots()
        sns.barplot(x=missing_values.index, y=missing_values.values, ax=ax)
        ax.set_xticks(range(len(missing_values.index)))  # Définit explicitement les ticks
        ax.set_xticklabels(missing_values.index, rotation=90)
        return fig
    return None

def plot_boxplot(df, col):
    """Génère une boîte à moustaches pour la colonne spécifiée."""
    fig, ax = plt.subplots()
    sns.boxplot(x=df[col], ax=ax, orient='v')
    return fig
