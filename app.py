# app.py
import streamlit as st
import os
import logging
import pandas as pd

# Importation des modules depuis src
from src.config import DEFAULT_SEPARATOR, DEFAULT_OUTPUT_DIR, DEFAULT_SAMPLE_NAME
from src.data_loader import load_data, sample_data
from src.eda import get_data_info
from src.eda_advanced import descriptive_stats, plot_distribution, plot_correlation, plot_missing_values, plot_boxplot
from src.utils import back_to_main
from src.treatments import rename_columns, fill_missing_values
from src.ui_upload import render_file_upload
from src.ui_utils import get_default_output_name, select_output_dir
from src.version import APP_NAME, NOM, VERSION, LAST_UPDATE, CONTACT, LATEST_FEATURES

# Configuration des logs
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------ Gestion de l'état de session ------------------
if 'df' not in st.session_state:
    st.session_state.df = None                   # DataFrame actuellement utilisé
if 'separator' not in st.session_state:
    st.session_state.separator = DEFAULT_SEPARATOR  # Séparateur par défaut pour CSV (lecture)
if 'encoding' not in st.session_state:
    st.session_state.encoding = 'utf-8'           # Encodage par défaut
if 'loaded' not in st.session_state:
    st.session_state.loaded = False              # Indique si un fichier a été chargé
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = {}       # Pour la sélection des colonnes en EDA
if 'selected_analyses' not in st.session_state:
    st.session_state.selected_analyses = {         # Options d'analyses EDA
        "Statistiques descriptives": True,
        "Distribution": False,
        "Corrélation": False,
        "Valeurs manquantes": False,
        "Boîtes à moustaches": False
    }
if 'mode' not in st.session_state:
    st.session_state.mode = None                 # Mode : None, "eda" ou "traitement"
if 'last_file' not in st.session_state:
    st.session_state.last_file = None            # Chemin du dernier fichier généré
if 'original_file_name' not in st.session_state:
    st.session_state.original_file_name = None   # Nom du fichier chargé initialement

# ------------------ Bouton Reset ------------------
if st.sidebar.button("Reset App"):
    st.session_state.clear()
    st.rerun()  # À partir de Streamlit 1.18, st.rerun() remplace st.experimental_rerun()

# ------------------ Titre et Sidebar ------------------
st.title(APP_NAME)
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown(f"""
---
**{APP_NAME}**  
**Développé par :** {NOM}  
**Version :** {VERSION}  
**Dernière mise à jour :** {LAST_UPDATE}  
**Contact :** {CONTACT}  

**Nouveautés de cette version :**
- {LATEST_FEATURES[0]}
- {LATEST_FEATURES[1]}
- {LATEST_FEATURES[2]}
- {LATEST_FEATURES[3]}
""")

# ------------------ Chargement du fichier ------------------
uploaded_file, detected_enc = render_file_upload()
if uploaded_file is not None:
    # Sélection de l'encodage et du séparateur (pour CSV)
    common_encodings = ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252", "ascii"]
    default_enc_index = common_encodings.index(detected_enc) if detected_enc in common_encodings else 0
    st.session_state.encoding = st.selectbox(
        "Choisir l'encodage du fichier",
        options=common_encodings,
        index=default_enc_index
    )
    if uploaded_file.name.endswith('.csv'):
        separators = [",", ";", "\\t", "|"]
        if st.session_state.separator in separators:
            default_sep_index = separators.index(st.session_state.separator)
        else:
            default_sep_index = 0
        st.session_state.separator = st.selectbox(
            "Choisir le séparateur CSV (lecture)",
            options=separators,
            index=default_sep_index
        )
    else:
        st.session_state.separator = None

    # Prévisualisation du fichier
    if st.button("Prévisualiser les données"):
        try:
            uploaded_file.seek(0)
            df_preview = load_data(uploaded_file, separator=st.session_state.separator, encoding=st.session_state.encoding)
            st.write("**Aperçu des données (5 premières lignes) :**")
            st.dataframe(df_preview.head(5), use_container_width=True)
        except Exception as e:
            st.error(f"Erreur lors de la prévisualisation : {e}")

    # Chargement complet du fichier
    if st.button("Charger le fichier complet") and not st.session_state.loaded:
        try:
            uploaded_file.seek(0)
            st.session_state.df = load_data(uploaded_file, separator=st.session_state.separator, encoding=st.session_state.encoding)
            st.session_state.loaded = True
            st.session_state.selected_columns = {col: True for col in st.session_state.df.columns}
            st.session_state.original_file_name = uploaded_file.name
            st.success("Fichier chargé avec succès !")
        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")

# ------------------ Affichage et Navigation ------------------
if st.session_state.loaded and st.session_state.df is not None:
    df = st.session_state.df

    st.subheader("Informations de base sur le dataset")
    st.dataframe(df.head(), use_container_width=True)
    info = get_data_info(df)
    st.markdown(f"**Dimensions :** {info['dimensions'][0]} lignes, {info['dimensions'][1]} colonnes")
    st.markdown("**Noms des colonnes :** " + ", ".join(info['column_names']))
    st.markdown("**Types de données :**")
    st.dataframe(pd.DataFrame(info['data_types'].items(), columns=['Colonne', 'Type']), use_container_width=True)
    st.markdown("**Valeurs manquantes par colonne :**")
    st.dataframe(pd.DataFrame(info['missing_values'].items(), columns=['Colonne', 'Valeurs manquantes']), use_container_width=True)
    original_size = df.memory_usage(deep=True).sum()
    st.write(f"**Taille estimée en mémoire :** {original_size / (1024 * 1024):.2f} Mo")

    # Option de réutilisation du fichier traité précédemment
    if st.session_state.last_file:
        use_last = st.checkbox("Utiliser le fichier généré précédemment", value=True)
        if use_last:
            try:
                df_new = load_data(
                    st.session_state.last_file,
                    separator=st.session_state.separator,  # Important : on relit avec le même séparateur choisi !
                    encoding=st.session_state.encoding
                )
                st.session_state.df = df_new
                df = df_new
                st.info(f"Fichier {st.session_state.last_file} chargé pour le traitement.")
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier généré : {e}")

    # Navigation entre EDA et Traitement
    if st.session_state.mode is None:
        st.subheader("Que souhaitez-vous faire ?")
        col1, col2 = st.columns(2)
        if col1.button("EDA +"):
            st.session_state.mode = "eda"
        if col2.button("Traitement"):
            st.session_state.mode = "traitement"

    # ------------------ Mode EDA+ ------------------
    if st.session_state.mode == "eda":
        st.subheader("Analyse Exploratoire Avancée (EDA+)")
        with st.form("eda_form"):
            st.write("**Sélectionnez les colonnes à analyser :**")
            for col in df.columns:
                st.session_state.selected_columns[col] = st.checkbox(
                    col, value=st.session_state.selected_columns.get(col, True), key=f"col_{col}"
                )
            st.write("**Sélectionnez les types d'analyse :**")
            analyses = ["Statistiques descriptives", "Distribution", "Corrélation", "Valeurs manquantes", "Boîtes à moustaches"]
            for analysis in analyses:
                st.session_state.selected_analyses[analysis] = st.checkbox(
                    analysis,
                    value=st.session_state.selected_analyses.get(analysis, False),
                    key=f"analysis_{analysis}"
                )
            submitted = st.form_submit_button("Appliquer EDA+")

        if submitted:
            st.subheader("Résultats de l'EDA+")
            selected_columns = [col for col, selected in st.session_state.selected_columns.items() if selected]
            if not selected_columns:
                st.warning("Veuillez sélectionner au moins une colonne.")
            else:
                df_selected = df[selected_columns]
                if st.session_state.selected_analyses.get("Statistiques descriptives", False):
                    st.write("**Statistiques descriptives :**")
                    st.dataframe(descriptive_stats(df_selected))
                if st.session_state.selected_analyses.get("Distribution", False):
                    numerical_cols = df_selected.select_dtypes(include=['float64', 'int64']).columns
                    for col in numerical_cols:
                        st.write(f"**Distribution de {col} :**")
                        fig = plot_distribution(df_selected, col)
                        st.pyplot(fig)
                if st.session_state.selected_analyses.get("Corrélation", False):
                    fig = plot_correlation(df_selected)
                    if fig:
                        st.write("**Matrice de corrélation :**")
                        st.pyplot(fig)
                    else:
                        st.write("Veuillez sélectionner au moins deux colonnes numériques pour la corrélation.")
                if st.session_state.selected_analyses.get("Valeurs manquantes", False):
                    fig = plot_missing_values(df_selected)
                    if fig:
                        st.write("**Visualisation des valeurs manquantes :**")
                        st.pyplot(fig)
                    else:
                        st.write("Aucune valeur manquante détectée.")
                if st.session_state.selected_analyses.get("Boîtes à moustaches", False):
                    numerical_cols = df_selected.select_dtypes(include=['float64', 'int64']).columns
                    for col in numerical_cols:
                        st.write(f"**Boîte à moustaches pour {col} :**")
                        fig = plot_boxplot(df_selected, col)
                        st.pyplot(fig)
        back_to_main()

    # ------------------ Mode Traitement ------------------
    if st.session_state.mode == "traitement":
        st.subheader("Traitements Disponibles")
        traitement = st.selectbox("Choisissez un traitement", ["Échantillonnage", "Renommage des colonnes", "Remplissage des valeurs null"])
        
        # --- Traitement : Échantillonnage ---
        if traitement == "Échantillonnage":
            st.subheader("Échantillonnage du dataset")
            method = st.selectbox("Méthode d’échantillonnage", ["random_total", "random_representatif", "first_n", "last_n"])
            if method in ["random_total", "random_representatif"]:
                choice = st.radio("Choisir le nombre de lignes", ["Pourcentage", "Nombre"])
                if choice == "Pourcentage":
                    percentage = st.slider("Pourcentage de lignes à échantillonner", 0, 100, 10)
                    frac = percentage / 100
                    n = None
                else:
                    n = st.number_input(
                        "Nombre de lignes à échantillonner", min_value=1, max_value=len(df), value=min(1000, len(df))
                    )
                    frac = None
            else:
                n = st.number_input("Nombre de lignes à échantillonner", min_value=1, max_value=len(df), value=min(1000, len(df)))
                frac = None
            
            output_dir = select_output_dir()
            default_output_name = get_default_output_name("echantillonnage")
            output_name = st.text_input("Nom du fichier de sortie", default_output_name)
            output_format = st.selectbox("Format de sortie", ["CSV", "Excel"])
            
            # Choix du séparateur spécifique pour l'export CSV
            export_separators = [",", ";", "\t", "|"]
            export_separator = st.selectbox(
                "Choisir le séparateur CSV pour l'exportation (si CSV)",
                options=export_separators,
                index=0
            )

            # Choix de l'encodage
            output_encoding = st.selectbox(
                "Choisir l'encodage pour le fichier de sortie",
                options=["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252", "ascii"],
                index=0
            )

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
                        # On utilise le séparateur choisi pour l'export CSV
                        df_sample.to_csv(output_path, index=False, encoding=output_encoding, sep=export_separator)
                    else:
                        output_path = os.path.join(output_dir, f"{output_name}.xlsx")
                        df_sample.to_excel(output_path, index=False)
                    
                    st.success(f"Fichier sauvegardé sous {output_path}")
                    st.session_state.last_file = output_path
                except Exception as e:
                    st.error(f"Erreur lors de l’échantillonnage : {e}")
        
        # --- Traitement : Renommage des colonnes ---
        elif traitement == "Renommage des colonnes":
            st.subheader("Renommage des colonnes")
            st.write("Modifiez les noms de colonnes ci-dessous :")
            with st.form("renommage_form"):
                new_names = {}
                for col in df.columns:
                    new_names[col] = st.text_input(f"Nouvel nom pour la colonne '{col}'", value=col)
                submit_rename = st.form_submit_button("Renommer les colonnes")
            if submit_rename:
                try:
                    df_renamed = rename_columns(df, new_names)
                    st.session_state.df = df_renamed
                    st.write("**Aperçu après renommage :**")
                    st.dataframe(df_renamed.head(), use_container_width=True)
                    output_dir = select_output_dir()
                    default_output_name = get_default_output_name("renommage")
                    output_name = st.text_input("Nom du fichier de sortie", default_output_name)
                    output_format = st.selectbox("Format de sortie", ["CSV", "Excel"])
                    output_encoding = st.selectbox(
                        "Choisir l'encodage pour le fichier de sortie",
                        options=["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252", "ascii"],
                        index=0
                    )
                    # Optionnel : un séparateur pour l'export CSV si voulu
                    export_separators = [",", ";", "\t", "|"]
                    export_separator = st.selectbox(
                        "Séparateur CSV (si CSV)",
                        options=export_separators,
                        index=0
                    )
                    if st.button("Enregistrer le fichier renommé"):
                        if output_format == "CSV":
                            output_path = os.path.join(output_dir, f"{output_name}.csv")
                            df_renamed.to_csv(output_path, index=False, encoding=output_encoding, sep=export_separator)
                        else:
                            output_path = os.path.join(output_dir, f"{output_name}.xlsx")
                            df_renamed.to_excel(output_path, index=False)
                        st.success(f"Fichier sauvegardé sous {output_path}")
                        st.session_state.last_file = output_path
                except Exception as e:
                    st.error(f"Erreur lors du renommage : {e}")
        
        # --- Traitement : Remplissage des valeurs null ---
        elif traitement == "Remplissage des valeurs null":
            st.subheader("Remplissage des valeurs null / NaN")
            st.write("**Nombre de valeurs null par colonne :**")
            missing_counts = df.isnull().sum()
            st.dataframe(
                missing_counts.reset_index().rename(columns={'index': 'Colonne', 0: 'Nombre de null'}),
                use_container_width=True
            )
            cols_with_null = missing_counts[missing_counts > 0].index.tolist()
            selected_cols = st.multiselect(
                "Sélectionnez les colonnes à traiter", 
                options=df.columns.tolist(), 
                default=cols_with_null
            )
            if selected_cols:
                method_option = st.selectbox(
                    "Sélectionnez la méthode de remplacement", 
                    options=["0", "mean", "median", "ffill", "bfill", "custom"]
                )
                custom_value = None
                if method_option == "custom":
                    custom_value = st.text_input("Entrez la valeur à utiliser pour le remplacement")
                if st.button("Remplir les valeurs null"):
                    try:
                        df_filled = fill_missing_values(df, selected_cols, method_option, custom_value)
                        st.session_state.df = df_filled
                        st.write("**Aperçu après remplissage :**")
                        st.dataframe(df_filled.head(), use_container_width=True)
                        output_dir = select_output_dir()
                        default_output_name = get_default_output_name("remplissage")
                        output_name = st.text_input("Nom du fichier de sortie", default_output_name)
                        output_format = st.selectbox("Format de sortie", ["CSV", "Excel"])
                        output_encoding = st.selectbox(
                            "Choisir l'encodage pour le fichier de sortie",
                            options=["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252", "ascii"],
                            index=0
                        )
                        # Optionnel : un séparateur pour l'export CSV
                        export_separators = [",", ";", "\t", "|"]
                        export_separator = st.selectbox(
                            "Séparateur CSV (si CSV)",
                            options=export_separators,
                            index=0
                        )
                        if st.button("Enregistrer le fichier traité"):
                            if output_format == "CSV":
                                output_path = os.path.join(output_dir, f"{output_name}.csv")
                                df_filled.to_csv(output_path, index=False, encoding=output_encoding, sep=export_separator)
                            else:
                                output_path = os.path.join(output_dir, f"{output_name}.xlsx")
                                df_filled.to_excel(output_path, index=False)
                            st.success(f"Fichier sauvegardé sous {output_path}")
                            st.session_state.last_file = output_path
                    except Exception as e:
                        st.error(f"Erreur lors du remplissage : {e}")
        back_to_main()
