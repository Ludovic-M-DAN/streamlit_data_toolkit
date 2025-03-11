import streamlit as st
from src.data_loader import load_data, sample_data
from src.eda import get_data_info
from src.eda_advanced import descriptive_stats, plot_distribution, plot_correlation, plot_missing_values, plot_boxplot
from src.utils import back_to_main
from src.config import DEFAULT_SEPARATOR, DEFAULT_OUTPUT_DIR, DEFAULT_SAMPLE_NAME
import pandas as pd
import os
import logging

# Configuration des logs pour enregistrer les erreurs dans un fichier 'app.log'
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialisation de l'état de session pour stocker les variables persistantes entre les interactions
if 'df' not in st.session_state:
    st.session_state.df = None  # DataFrame chargé (sera rempli une fois le fichier uploadé)
if 'separator' not in st.session_state:
    st.session_state.separator = DEFAULT_SEPARATOR  # Séparateur par défaut pour les fichiers CSV
if 'loaded' not in st.session_state:
    st.session_state.loaded = False  # Indique si un fichier a été chargé ou non
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = {}  # Dictionnaire des colonnes sélectionnées pour l'analyse EDA
if 'selected_analyses' not in st.session_state:
    st.session_state.selected_analyses = {
        "Statistiques descriptives": True,  # Activé par défaut
        "Distribution": False,
        "Corrélation": False,
        "Valeurs manquantes": False,
        "Boîtes à moustaches": False
    }  # Types d'analyses EDA sélectionnés par l'utilisateur
if 'mode' not in st.session_state:
    st.session_state.mode = None  # Mode actuel de l'application : None (menu principal), "eda" ou "traitement"

# Titre principal de l'application affiché en haut de la page
st.title("Data Toolkit")

# Ajout du logo dans la barre latérale, en haut à gauche
st.sidebar.image("logo.png", use_container_width=True)  # Affiche le fichier 'logo.png' en ajustant sa largeur à la sidebar

# Ajout des informations dans la barre latérale, sous le logo
st.sidebar.markdown("""
---
**Développé par :** Ludovic Marchetti  
**Version :** 1.0  
**Dernière mise à jour :** 11/03/2025  
**Contact :** contact@datahootcome.fr
""")

# Section pour télécharger un fichier (CSV ou Excel)
uploaded_file = st.file_uploader("Déposez votre fichier ici", type=['csv', 'xlsx'])

# Si un fichier est téléchargé, proposer des options de prévisualisation et de chargement
if uploaded_file is not None:
    # Si le fichier est un CSV, demander à l'utilisateur de spécifier le séparateur
    if uploaded_file.name.endswith('.csv'):
        st.session_state.separator = st.text_input(
            "Entrez le séparateur utilisé dans le fichier CSV (ex: ',', ';', '\\t')", 
            value=st.session_state.separator
        )
    else:
        st.session_state.separator = None  # Pas besoin de séparateur pour un fichier Excel

    # Bouton pour prévisualiser les 5 premières lignes du fichier
    if st.button("Prévisualiser les données"):
        try:
            uploaded_file.seek(0)  # Remet le pointeur au début du fichier pour le lire
            if uploaded_file.name.endswith('.csv'):
                df_preview = pd.read_csv(uploaded_file, sep=st.session_state.separator, nrows=5)
            else:
                df_preview = pd.read_excel(uploaded_file, nrows=5)
            st.write("**Aperçu des données :**")
            st.dataframe(df_preview, use_container_width=True)  # Affiche les 5 premières lignes
        except Exception as e:
            logging.error(f"Erreur lors de la prévisualisation : {e}")  # Enregistre l'erreur dans 'app.log'
            st.error(f"Erreur lors de la prévisualisation : {e}")  # Affiche l'erreur à l'utilisateur

    # Bouton pour charger le fichier complet dans l'application
    if st.button("Charger le fichier complet") and not st.session_state.loaded:
        try:
            uploaded_file.seek(0)  # Remet le pointeur au début du fichier
            st.session_state.df = load_data(uploaded_file, separator=st.session_state.separator)  # Charge le fichier avec la fonction load_data
            st.session_state.loaded = True  # Marque le fichier comme chargé
            st.session_state.selected_columns = {col: True for col in st.session_state.df.columns}  # Sélectionne toutes les colonnes par défaut
            st.success("Fichier chargé avec succès !")  # Confirme le succès à l'utilisateur
        except Exception as e:
            logging.error(f"Erreur lors du chargement : {e}")
            st.error(f"Erreur lors du chargement : {e}")

# Si un fichier est chargé, afficher les informations et proposer des actions
if st.session_state.loaded and st.session_state.df is not None:
    df = st.session_state.df  # Récupère le DataFrame chargé

    # Afficher un aperçu et des informations de base sur le dataset
    st.subheader("Informations de base sur le dataset")
    st.dataframe(df.head(), use_container_width=True)  # Affiche les 5 premières lignes du dataset
    info = get_data_info(df)  # Récupère les informations de base avec la fonction get_data_info
    st.markdown(f"**Dimensions :** {info['dimensions'][0]} lignes, {info['dimensions'][1]} colonnes")
    st.markdown("**Noms des colonnes :**")
    st.write(", ".join(info['column_names']))  # Liste les noms des colonnes
    st.markdown("**Types de données :**")
    st.dataframe(pd.DataFrame(info['data_types'].items(), columns=['Colonne', 'Type']), use_container_width=True)
    st.markdown("**Valeurs manquantes par colonne :**")
    st.dataframe(pd.DataFrame(info['missing_values'].items(), columns=['Colonne', 'Valeurs manquantes']), use_container_width=True)
    original_size = df.memory_usage(deep=True).sum()  # Calcule la taille en mémoire du DataFrame
    st.write(f"**Taille estimée en mémoire :** {original_size / (1024 * 1024):.2f} Mo")

    # Si aucun mode n'est sélectionné, proposer un choix entre EDA+ et Traitement
    if st.session_state.mode is None:
        st.subheader("Que souhaitez-vous faire ?")
        col1, col2 = st.columns(2)  # Crée deux colonnes pour les boutons
        if col1.button("EDA +"):
            st.session_state.mode = "eda"  # Passe en mode EDA+
        if col2.button("Traitement"):
            st.session_state.mode = "traitement"  # Passe en mode Traitement

    # --- Mode EDA+ : Exploration de données avancée ---
    if st.session_state.mode == "eda":
        st.subheader("Paramétrer l'EDA avancé")
        with st.form("eda_form"):  # Crée un formulaire pour les paramètres de l'EDA
            # Sélection des colonnes à analyser
            st.write("**Sélectionnez les colonnes à analyser :**")
            for col in df.columns:
                st.session_state.selected_columns[col] = st.checkbox(
                    col, 
                    value=st.session_state.selected_columns.get(col, True), 
                    key=f"col_{col}"
                )  # Crée une checkbox pour chaque colonne, cochée par défaut
            # Sélection des types d'analyse à effectuer
            st.write("**Sélectionnez les types d'analyse :**")
            analyses = ["Statistiques descriptives", "Distribution", "Corrélation", "Valeurs manquantes", "Boîtes à moustaches"]
            for analysis in analyses:
                st.session_state.selected_analyses[analysis] = st.checkbox(
                    analysis, 
                    value=st.session_state.selected_analyses.get(analysis, False), 
                    key=f"analysis_{analysis}"
                )  # Crée une checkbox pour chaque type d'analyse
            submitted = st.form_submit_button("Appliquer EDA +")  # Bouton pour lancer l'EDA
    
        # Si le formulaire est soumis, afficher les résultats de l'EDA
        if submitted:
            st.subheader("Résultats de l'EDA avancé")
            selected_columns = [col for col, selected in st.session_state.selected_columns.items() if selected]
            if not selected_columns:
                st.warning("Veuillez sélectionner au moins une colonne.")
            else:
                df_selected = df[selected_columns]  # Filtre le DataFrame avec les colonnes sélectionnées
                # Statistiques descriptives
                if st.session_state.selected_analyses.get("Statistiques descriptives", False):
                    st.write("**Statistiques descriptives :**")
                    st.dataframe(descriptive_stats(df_selected))  # Affiche les stats descriptives
                # Distribution
                if st.session_state.selected_analyses.get("Distribution", False):
                    numerical_cols = df_selected.select_dtypes(include=['float64', 'int64']).columns
                    for col in numerical_cols:
                        st.write(f"**Distribution de {col} :**")
                        fig = plot_distribution(df_selected, col)  # Génère un graphique de distribution
                        st.pyplot(fig)  # Affiche le graphique
                # Corrélation
                if st.session_state.selected_analyses.get("Corrélation", False):
                    fig = plot_correlation(df_selected)  # Génère une matrice de corrélation
                    if fig:
                        st.write("**Matrice de corrélation :**")
                        st.pyplot(fig)
                    else:
                        st.write("**Corrélation :** Sélectionnez au moins deux colonnes numériques.")
                # Valeurs manquantes
                if st.session_state.selected_analyses.get("Valeurs manquantes", False):
                    fig = plot_missing_values(df_selected)  # Génère un graphique des valeurs manquantes
                    if fig:
                        st.write("**Valeurs manquantes :**")
                        st.pyplot(fig)
                    else:
                        st.write("Aucune valeur manquante dans les colonnes sélectionnées.")
                # Boîtes à moustaches
                if st.session_state.selected_analyses.get("Boîtes à moustaches", False):
                    numerical_cols = df_selected.select_dtypes(include=['float64', 'int64']).columns
                    for col in numerical_cols:
                        st.write(f"**Boîte à moustaches pour {col} :**")
                        fig = plot_boxplot(df_selected, col)  # Génère une boîte à moustaches
                        st.pyplot(fig)
        # Bouton pour revenir au menu principal
        back_to_main()

    # --- Mode Traitement : Manipulation des données ---
    if st.session_state.mode == "traitement":
        st.subheader("Traitements disponibles")
        traitement = st.selectbox("Choisissez un traitement", ["Échantillonnage"])  # Pour l'instant, seul l'échantillonnage est proposé
        if traitement == "Échantillonnage":
            st.subheader("Échantillonnage du dataset")
            method = st.selectbox("Méthode d’échantillonnage", 
                                  ["random_total", "random_representatif", "first_n", "last_n"])
            # Options pour les méthodes aléatoires
            if method in ["random_total", "random_representatif"]:
                choice = st.radio("Choisir le nombre de lignes", ["Pourcentage", "Nombre"])
                if choice == "Pourcentage":
                    percentage = st.slider("Pourcentage de lignes à échantillonner", 0, 100, 10)
                    frac = percentage / 100  # Convertit le pourcentage en fraction
                    n = None
                else:
                    n = st.number_input("Nombre de lignes à échantillonner", min_value=1, max_value=len(df), value=min(1000, len(df)))
                    frac = None
            else:  # Pour "first_n" ou "last_n"
                n = st.number_input("Nombre de lignes à échantillonner", min_value=1, max_value=len(df), value=min(1000, len(df)))
                frac = None

            # Champ pour spécifier le dossier de destination
            output_dir = st.text_input(
                "Chemin du dossier de destination (laisser vide pour utiliser 'output' par défaut)", 
                value=""
            )
            
            # Gestion du dossier de sortie
            if not output_dir:
                output_dir = os.path.join(os.getcwd(), "output")  # Utilise le dossier 'output' par défaut
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)  # Crée le dossier s'il n'existe pas
                st.info(f"Utilisation du dossier par défaut : {output_dir}")
            else:
                st.info(f"Utilisation du dossier personnalisé : {output_dir}")
            
            output_name = st.text_input("Nom du fichier de sortie", DEFAULT_SAMPLE_NAME)  # Nom par défaut du fichier
            output_format = st.selectbox("Format de sortie", ["CSV", "Excel"])  # Choix du format

            # Bouton pour lancer l'échantillonnage
            if st.button("Échantillonner"):
                try:
                    df_sample = sample_data(df, method, n, frac)  # Génère l'échantillon avec la fonction sample_data
                    st.write("**Aperçu de l’échantillon :**")
                    st.dataframe(df_sample.head(), use_container_width=True)
                    st.write(f"**Dimensions de l'échantillon :** {df_sample.shape[0]} lignes, {df_sample.shape[1]} colonnes")
                    sample_size = df_sample.memory_usage(deep=True).sum()
                    st.write(f"**Taille estimée en mémoire de l'échantillon :** {sample_size / (1024 * 1024):.2f} Mo")
                    if output_format == "CSV":
                        output_path = os.path.join(output_dir, f"{output_name}.csv")
                        df_sample.to_csv(output_path, index=False)  # Sauvegarde en CSV
                        st.success(f"Fichier sauvegardé sous {output_path}")
                    else:
                        output_path = os.path.join(output_dir, f"{output_name}.xlsx")
                        df_sample.to_excel(output_path, index=False)  # Sauvegarde en Excel
                        st.success(f"Fichier sauvegardé sous {output_path}")
                except Exception as e:
                    logging.error(f"Erreur lors de l’échantillonnage : {e}")
                    st.error(f"Erreur lors de l’échantillonnage : {e}")
        # Bouton pour revenir au menu principal
        back_to_main()