import streamlit as st

def back_to_main():
    """Affiche un bouton 'Retour' qui réinitialise le mode à None."""
    if st.button("Retour"):
        st.session_state.mode = None