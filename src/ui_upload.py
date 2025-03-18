# ui_upload.py
import streamlit as st
import chardet

def detect_encoding(file):
    """
    Détecte l'encodage d'un fichier via un échantillon.
    
    :param file: Objet fichier (ex: UploadedFile de Streamlit)
    :return: Encodage détecté (ex: 'utf-8', 'iso-8859-1', etc.)
    """
    file.seek(0)
    sample = file.read(1024)
    result = chardet.detect(sample)
    return result['encoding']

def render_file_upload():
    """
    Affiche le widget d'upload et gère la détection d'encodage.
    
    :return: Tuple (uploaded_file, detected_encoding) ou (None, None)
    """
    uploaded_file = st.file_uploader("Déposez votre fichier ici", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        try:
            detected_enc = detect_encoding(uploaded_file)
            st.info(f"Encodage détecté : {detected_enc}")
        except Exception as e:
            st.error(f"Erreur lors de la détection de l'encodage : {e}")
            detected_enc = 'utf-8'
        return uploaded_file, detected_enc
    return None, None
