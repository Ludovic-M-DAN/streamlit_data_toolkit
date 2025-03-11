import streamlit as st
from src.data_loader import load_data, sample_data
from src.eda import get_data_info
from src.eda_advanced import descriptive_stats, plot_distribution, plot_correlation, plot_missing_values, plot_boxplot
from src.utils import back_to_main
from src.config import DEFAULT_SEPARATOR, DEFAULT_OUTPUT_DIR, DEFAULT_SAMPLE_NAME
import pandas as pd
import os
import logging
import chardet

# Configuration des logs pour enregistrer les erreurs dans un fichier 'app.log'
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialisation de l'état de session pour stocker les variables persistantes entre les interactions
if 'df' not in st.session_state:
    st.session_state.df = None  # DataFrame chargé (sera rempli une fois le fichier uploadé)
if 'separator' not in st.session_state:
    st.session_state.separator = DEFAULT_SEPARATOR  # Séparateur par défaut pour les fichiers CSV
if 'encoding' not in st.session_state:
    st.session_state.encoding = 'utf-8'  # Encodage par défaut
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

# Fonction pour détecter l'encodage du fichier
def detect_encoding(file):
    """
    Détecte l'encodage d'un fichier via un échantillon (chardet).
    
    :param file: Objet fichier (ex. uploaded_file de Streamlit)
    :return: Encodage détecté (ex: 'utf-8', 'iso-8859-1', 'ascii')
    """
    file.seek(0)  # Remettre le curseur au début du fichier
    sample = file.read(1024)  # Lire un échantillon
    result = chardet.detect(sample)
    return result['encoding']

# Titre principal de l'application
st.title("Data Toolkit")

# Ajout du logo dans la barre latérale
st.sidebar.image("logo.png", use_container_width=True)

# Infos dans la barre latérale
st.sidebar.markdown("""
---
**Développé par :** Ludovic Marchetti  
**Version :** 1.0.1  
**Dernière mise à jour :** 12/03/2025  
**Contact :** contact@datahootcome.fr
""")

# Section pour télécharger un fichier (CSV ou Excel)
uploaded_file = st.file_uploader("Déposez votre fichier ici", type=['csv', 'xlsx'])

# Si un fichier est téléchargé, proposer des options de prévisualisation et de chargement
if uploaded_file is not None:
    try:
        # Détection automatique de l'encodage
        detected_enc = detect_encoding(uploaded_file)
        st.info(f"Encodage détecté (chardet) : {detected_enc}")
    except Exception as e:
        st.error(f"Erreur lors de la détection de l'encodage : {e}")
        detected_enc = 'utf-8'

    # <-- MODIF: Liste déroulante d'encodages courants
    common_encodings = ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252", "ascii"]
    # On essaie de trouver l'index du detected_enc dans la liste, sinon on met 0
    if detected_enc in common_encodings:
        default_enc_index = common_encodings.index(detected_enc)
    else:
        default_enc_index = 0  # 'utf-8' en fallback

    st.session_state.encoding = st.selectbox(
        "Choisir l'encodage du fichier",
        options=common_encodings,
        index=default_enc_index
    )

    # Si le fichier est un CSV, demander un séparateur
    if uploaded_file.name.endswith('.csv'):
        # <-- MODIF: Liste déroulante de séparateurs classiques
        separators = [",", ";", "\\t", "|"]
        # On détecte si st.session_state.separator est dans la liste, sinon on met 0
        if st.session_state.separator in separators:
            default_sep_index = separators.index(st.session_state.separator)
        else:
            default_sep_index = 0

        st.session_state.separator = st.selectbox(
            "Choisir le séparateur CSV",
            options=separators,
            index=default_sep_index
        )
    else:
        # Fichier Excel -> pas de séparateur
        st.session_state.separator = None

    # Bouton pour prévisualiser
    if st.button("Prévisualiser les données"):
        try:
            uploaded_file.seek(0)  # Remet le pointeur au début
            df_preview = load_data(
                uploaded_file,
                separator=st.session_state.separator,
                encoding=st.session_state.encoding
            )
            st.write("**Aperçu des données (5 premières lignes) :**")
            st.dataframe(df_preview.head(5), use_container_width=True)
        except Exception as e:
            logging.error(f"Erreur lors de la prévisualisation : {e}")
            st.error(f"Erreur lors de la prévisualisation : {e}")

    # Bouton pour charger le fichier complet
    if st.button("Charger le fichier complet") and not st.session_state.loaded:
        try:
            uploaded_file.seek(0)
            st.session_state.df = load_data(
                uploaded_file,
                separator=st.session_state.separator,
                encoding=st.session_state.encoding
            )
            st.session_state.loaded = True
            st.session_state.selected_columns = {
                col: True for col in st.session_state.df.columns
            }
            st.success("Fichier chargé avec succès !")
        except Exception as e:
            logging.error(f"Erreur lors du chargement : {e}")
            st.error(f"Erreur lors du chargement : {e}")

# Si un fichier est chargé, afficher des infos et proposer actions
if st.session_state.loaded and st.session_state.df is not None:
    df = st.session_state.df

    # Aperçu + infos de base
    st.subheader("Informations de base sur le dataset")
    st.dataframe(df.head(), use_container_width=True)
    info = get_data_info(df)
    st.markdown(f"**Dimensions :** {info['dimensions'][0]} lignes, {info['dimensions'][1]} colonnes")
    st.markdown("**Noms des colonnes :**")
    st.write(", ".join(info['column_names']))
    st.markdown("**Types de données :**")
    st.dataframe(pd.DataFrame(info['data_types'].items(), columns=['Colonne', 'Type']), use_container_width=True)
    st.markdown("**Valeurs manquantes par colonne :**")
    st.dataframe(pd.DataFrame(info['missing_values'].items(), columns=['Colonne', 'Valeurs manquantes']), use_container_width=True)
    original_size = df.memory_usage(deep=True).sum()
    st.write(f"**Taille estimée en mémoire :** {original_size / (1024 * 1024):.2f} Mo")

    # Choix du mode
    if st.session_state.mode is None:
        st.subheader("Que souhaitez-vous faire ?")
        col1, col2 = st.columns(2)
        if col1.button("EDA +"):
            st.session_state.mode = "eda"
        if col2.button("Traitement"):
            st.session_state.mode = "traitement"

    # --- Mode EDA+ ---
    if st.session_state.mode == "eda":
        st.subheader("Paramétrer l'EDA avancé")
        with st.form("eda_form"):
            st.write("**Sélectionnez les colonnes à analyser :**")
            for col in df.columns:
                st.session_state.selected_columns[col] = st.checkbox(
                    col,
                    value=st.session_state.selected_columns.get(col, True),
                    key=f"col_{col}"
                )
            st.write("**Sélectionnez les types d'analyse :**")
            analyses = ["Statistiques descriptives", "Distribution", "Corrélation", "Valeurs manquantes", "Boîtes à moustaches"]
            for analysis in analyses:
                st.session_state.selected_analyses[analysis] = st.checkbox(
                    analysis,
                    value=st.session_state.selected_analyses.get(analysis, False),
                    key=f"analysis_{analysis}"
                )
            submitted = st.form_submit_button("Appliquer EDA +")
    
        if submitted:
            st.subheader("Résultats de l'EDA avancé")
            selected_columns = [col for col, selected in st.session_state.selected_columns.items() if selected]
            if not selected_columns:
                st.warning("Veuillez sélectionner au moins une colonne.")
            else:
                df_selected = df[selected_columns]
                # Statistiques descriptives
                if st.session_state.selected_analyses.get("Statistiques descriptives", False):
                    st.write("**Statistiques descriptives :**")
                    st.dataframe(descriptive_stats(df_selected))
                # Distribution
                if st.session_state.selected_analyses.get("Distribution", False):
                    numerical_cols = df_selected.select_dtypes(include=['float64', 'int64']).columns
                    for col in numerical_cols:
                        st.write(f"**Distribution de {col} :**")
                        fig = plot_distribution(df_selected, col)
                        st.pyplot(fig)
                # Corrélation
                if st.session_state.selected_analyses.get("Corrélation", False):
                    fig = plot_correlation(df_selected)
                    if fig:
                        st.write("**Matrice de corrélation :**")
                        st.pyplot(fig)
                    else:
                        st.write("**Corrélation :** Sélectionnez au moins deux colonnes numériques.")
                # Valeurs manquantes
                if st.session_state.selected_analyses.get("Valeurs manquantes", False):
                    fig = plot_missing_values(df_selected)
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
                        fig = plot_boxplot(df_selected, col)
                        st.pyplot(fig)
        back_to_main()

    # --- Mode Traitement ---
    if st.session_state.mode == "traitement":
        st.subheader("Traitements disponibles")
        traitement = st.selectbox("Choisissez un traitement", ["Échantillonnage"])
        if traitement == "Échantillonnage":
            st.subheader("Échantillonnage du dataset")
            method = st.selectbox("Méthode d’échantillonnage", 
                                  ["random_total", "random_representatif", "first_n", "last_n"])
            if method in ["random_total", "random_representatif"]:
                choice = st.radio("Choisir le nombre de lignes", ["Pourcentage", "Nombre"])
                if choice == "Pourcentage":
                    percentage = st.slider("Pourcentage de lignes à échantillonner", 0, 100, 10)
                    frac = percentage / 100
                    n = None
                else:
                    n = st.number_input("Nombre de lignes à échantillonner", min_value=1, max_value=len(df), value=min(1000, len(df)))
                    frac = None
            else:
                n = st.number_input("Nombre de lignes à échantillonner", min_value=1, max_value=len(df), value=min(1000, len(df)))
                frac = None

            output_dir = st.text_input(
                "Chemin du dossier de destination (laisser vide pour utiliser 'output' par défaut)", 
                value=""
            )
            
            if not output_dir:
                output_dir = os.path.join(os.getcwd(), "output")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                st.info(f"Utilisation du dossier par défaut : {output_dir}")
            else:
                st.info(f"Utilisation du dossier personnalisé : {output_dir}")
            
            output_name = st.text_input("Nom du fichier de sortie", DEFAULT_SAMPLE_NAME)
            output_format = st.selectbox("Format de sortie", ["CSV", "Excel"])

            if st.button("Échantillonner"):
                try:
                    df_sample = sample_data(df, method, n, frac)
                    st.write("**Aperçu de l’échantillon :**")
                    st.dataframe(df_sample.head(), use_container_width=True)
                    st.write(f"**Dimensions de l'échantillon :** {df_sample.shape[0]} lignes, {df_sample.shape[1]} colonnes")
                    sample_size = df_sample.memory_usage(deep=True).sum()
                    st.write(f"**Taille estimée en mémoire de l'échantillon :** {sample_size / (1024 * 1024):.2f} Mo")
                    if output_format == "CSV":
                        output_path = os.path.join(output_dir, f"{output_name}.csv")
                        df_sample.to_csv(output_path, index=False)
                        st.success(f"Fichier sauvegardé sous {output_path}")
                    else:
                        output_path = os.path.join(output_dir, f"{output_name}.xlsx")
                        df_sample.to_excel(output_path, index=False)
                        st.success(f"Fichier sauvegardé sous {output_path}")
                except Exception as e:
                    logging.error(f"Erreur lors de l’échantillonnage : {e}")
                    st.error(f"Erreur lors de l’échantillonnage : {e}")
        back_to_main()
