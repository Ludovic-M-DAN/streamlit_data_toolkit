# Data Toolkit 
Une application Streamlit interactive pour explorer, analyser et traiter des fichiers CSV ou Excel.

## Description
Cette application Streamlit a été conçue pour simplifier l’analyse de données. Elle permet de charger facilement des fichiers CSV ou Excel, de prévisualiser leur contenu et de réaliser des **analyses exploratoires (EDA)** adaptées à vos besoins. Vous pouvez aussi appliquer des **traitements** comme l’échantillonnage ou le filtrage, rendant la manipulation des datasets plus fluide.

**Motivation** : L’objectif est de réunir dans une interface conviviale les étapes courantes de l’analyse de données, souvent éparpillées dans des notebooks ou des scripts. Fini les recherches de code ou les réécritures inutiles : cette appli vous fait gagner du temps pour vous focaliser sur ce qui compte vraiment, l’interprétation des résultats.

## Fonctions de la V1

### Fonctions de base
- **Chargement du dataset** : Importation de fichiers CSV ou Excel (jusqu’à 5 Go).
- **Choix du séparateur** : Sélection manuelle du séparateur pour les fichiers CSV (ex. `,`, `;`, `\t`).
- **Prévisualisation des données** : Affichage des premières lignes pour un aperçu rapide avant chargement complet.
- **Chargement complet des données** : Importation du dataset entier pour analyse ou traitement.
- **Informations de base sur les données** : Affichage des détails essentiels :
  - Dimensions (nombre de lignes et colonnes).
  - Noms et types des colonnes.
  - Valeurs manquantes par colonne.
  - Taille en mémoire.
- **Sauvegarde après traitement** : Exportation du fichier modifié (CSV ou Excel) dans un dossier personnalisé ou par défaut ("output").

### Fonctions avancées
- **EDA+ (Exploration avancée des données)** :
  - Statistiques descriptives : Moyenne, médiane, min, max, écart-type, etc.
  - Visualisations : Histogrammes (distributions), matrices de corrélation, boîtes à moustaches (détection des valeurs aberrantes), graphes des valeurs manquantes.
  - Personnalisation : Choix des colonnes et des types d’analyse.
- **Échantillonnage** :
  - Méthodes disponibles : Aléatoire (total ou représentatif), premières ou dernières N lignes.
  - Options : Sélection par pourcentage ou nombre exact de lignes.
  - Exportation : Sauvegarde de l’échantillon généré.
    
## Technologies
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)

## Comment l’utiliser ?
1. Clone le dépôt : `git clone https://github.com/ton-utilisateur/ton-projet.git`
2. Installe les dépendances : `pip install -r requirements.txt`
3. Lance l’app : `streamlit run app.py`
