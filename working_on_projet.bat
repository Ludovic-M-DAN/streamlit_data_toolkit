@echo off
echo =========================================
echo Activation de l'environnement virtuel et navigation vers le projet...
echo =========================================

:: Navigue vers le dossier du projet
cd /d "C:\Users\ludov\streamlit_data_toolkit"

:: Active l'environnement virtuel
call venv\Scripts\activate

echo.
echo =========================================
echo Récupération et mise à jour du dépôt GitHub
echo =========================================
echo - git pull
echo.
git pull

echo.
echo =========================================
echo Commandes Git pour contribuer
echo =========================================
echo Pour effectuer un commit :
echo 1. Ajouter les fichiers modifies : git add .
echo 2. Committer avec un message : git commit -m "votre message de commit"
echo 3. Pousser les changements : git push
echo.
echo Pour créer une pull request :
echo 1. Assurez-vous d\'avoir une branche dediee : git checkout -b feature/ma-branche
echo 2. Effectuez vos commits et push : git push origin feature/ma-branche
echo 3. Sur GitHub, ouvrez une Pull Request depuis la branche feature/ma-branche
echo.
echo Lorsque vous avez fini, fermez simplement cette fenêtre si vous le souhaitez ou continuez à exécuter des commandes git.

:: Ouvre une nouvelle invite de commandes avec l'environnement activé
cmd /k
