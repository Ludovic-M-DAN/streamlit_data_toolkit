# ui_utils.py
import os
import streamlit as st
from src.config import DEFAULT_OUTPUT_DIR

def get_default_output_name(treatment_suffix):
    """
    Construit un nom de fichier par défaut sous la forme "nomdufichier_nomdutraitement".
    
    Utilise le dernier fichier généré ou le nom original stocké dans st.session_state.
    
    :param treatment_suffix: Suffixe pour le traitement (ex: "echantillonnage", "renommage", "remplissage")
    :return: Nom de fichier par défaut (sans extension)
    """
    if "last_file" in st.session_state and st.session_state.last_file:
        base = os.path.splitext(os.path.basename(st.session_state.last_file))[0]
    elif "original_file_name" in st.session_state and st.session_state.original_file_name:
        base = os.path.splitext(st.session_state.original_file_name)[0]
    else:
        base = "output"
    return f"{base}_{treatment_suffix}"

def select_output_dir():
    """
    Permet de sélectionner le répertoire de destination.
    
    Si l'utilisateur ne renseigne pas de chemin, on utilise le répertoire par défaut relatif à l'application.
    
    :return: Chemin du répertoire de sortie
    """
    output_dir = st.text_input("Chemin du dossier de destination (laisser vide pour utiliser le dossier par défaut)", value="")
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(__file__), DEFAULT_OUTPUT_DIR)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        st.info(f"Utilisation du dossier par défaut : {output_dir}")
    else:
        st.info(f"Utilisation du dossier personnalisé : {output_dir}")
    return output_dir
