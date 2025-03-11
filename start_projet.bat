@echo off
echo Activation de l'environnement virtuel et navigation vers le projet...

:: Navigue vers le dossier du projet
cd /d "C:\Users\ludov\streamlit_data_toolkit"

:: Active l'environnement virtuel
call venv\Scripts\activate

:: Ouvre une nouvelle invite de commandes avec l'environnement activé
cmd /k