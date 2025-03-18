# <img src="logo.png" alt="Logo" width="40" style="vertical-align: text-bottom;"/> Data Toolkit

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

**Data Toolkit** est une application interactive Streamlit qui simplifie l'exploration, l'analyse et le traitement de fichiers CSV ou Excel. Elle s'adresse aux data scientists, analystes ou toute personne souhaitant explorer ses données via une interface intuitive, sans avoir a charger un notebook et le laisser à l'abandon avec les autres (😉).

## 🌱 La genése 
À l'origine, je souhaitais simplement disposer d'un outil rapide pour visualiser le contenu d'un dataset. Par la suite, ayant eu besoin d'échantillonner un fichier CSV volumineux (> 3 Go), j'ai intégré cette fonctionnalité au premier outil. Et pourquoi s'arrêter en si bon chemin ? J'ai donc ajouté des analyses exploratoires basiques, ainsi que des analyses un peu plus poussées permettant de visualiser clairement les données. Ainsi est née la V1.

## ⚙️ Fonctionnalités

### Basiques
- **Chargement** : Import de fichiers CSV/Excel (jusqu’à 5 Go) avec séparateur personnalisé.
- **Prévisualisation** : Aperçu des 5 premières lignes avant chargement complet.
- **EDA simple** : Dimensions, types de colonnes, valeurs manquantes, taille en mémoire.

### Avancées
- **EDA+** : Statistiques descriptives, visualisations (histogrammes, corrélations, boîtes à moustaches, valeurs manquantes).
- **Personnalisation** : Choix des colonnes et des analyses.
- **Logs** : Gestion des erreurs dans app.log.
- **Traitement** : Échantillonnage (aléatoire, premières/dernières N lignes) avec export.

## 📂 Structure du Repository
```
streamlit_data_toolkit/
├── data/                   # Datasets d’exemple
├── docs/                   # Documentation détaillée (guides, API, etc.)
├── src/                    # Code source
│   ├── config.py           # Paramètres de configuration
│   ├── data_loader.py      # Fonctions de chargement et d'échantillonnage
│   ├── eda.py              # Fonctions d'analyse exploratoire (EDA)
│   ├── eda_advanced.py     # Visualisations avancées (histogrammes, heatmaps, etc.)
│   ├── treatments.py       # Fonctions de traitement (renommage, remplissage, etc.)
│   ├── ui_upload.py        # Gestion de l'upload et détection d'encodage
│   ├── ui_utils.py         # Fonctions UI utilitaires (choix du dossier, nom par défaut)
│   ├── version.py          # Informations de version et nouveautés
├── CHANGELOG.md            # Historique des modifications et nouveautés
├── app.py                  # Application principale (Streamlit)
├── README.md               # Présentation du projet
├── requirements.txt        # Dépendances
└── logo.png                # Logo de l'application
```

## 🛠️ Installation

1. **Cloner le repo** :
   ```bash
   git clone https://github.com/Ludovic-M-DAN/streamlit_data_toolkit.git
   cd streamlit_data_toolkit
   ```

2. **Créer un environnement virtuel (optionnel)** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l’app en augmentant la limite de fichier a 5Go** :
   ```bash
   streamlit run app.py --server.maxUploadSize=5000
   ```

Ouvrez [http://localhost:8501](http://localhost:8501) dans votre navigateur.

### :accessibility: Astuce rapide pour ne pas se compliquer la vie
Pour lancer l’application rapidement, créez un fichier batch `run_app.bat` à la racine du projet avec le contenu suivant :

```bat
@echo off

:: Créer un environnement virtuel
python -m venv venv

:: Activer l'environnement virtuel
call venv\Scripts\activate

:: Installer les dépendances
pip install -r requirements.txt

:: Lancer l'application Streamlit avec une limite de fichier de 5 Go
start "" http://localhost:8501
streamlit run app.py --server.maxUploadSize=5000

:: Mettre en pause pour voir les éventuelles erreurs
pause

```

## 📦 Dépendances principales
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10.1-11557C?style=flat&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13.2-4E148C?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.43.1-FF4B4B?style=flat&logo=streamlit&logoColor=white)

Le projet repose sur les bibliothèques suivantes :
- **[Python](https://www.python.org/)** (>= 3.7)
- **[Streamlit](https://streamlit.io/)** (1.43.1) – Interface interactive
- **[Pandas](https://pandas.pydata.org/)** (2.2.3) – Manipulation des données
- **[Matplotlib](https://matplotlib.org/)** (3.10.1) – Visualisation basique
- **[Seaborn](https://seaborn.pydata.org/)** (0.13.2) – Visualisation avancée
- **[NumPy](https://numpy.org/)** (2.2.3) – Calcul scientifique
- **[OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)** (3.1.5) – Gestion des fichiers Excel
- **[PyArrow](https://arrow.apache.org/)** (19.0.1) – Support des formats optimisés

Pour voir toutes les dépendances, consultez le fichier [`requirements.txt`](requirements.txt).

## 📖 Documentation
🚧 En cours de construction 🚧

## 🎥 Vidéo
🎬 ![Vidéo](https://img.shields.io/badge/Video-Play-green?style=flat&logo=youtube&logoColor=white)  
[📽️ Regarder la démo](https://youtu.be/oglqO8-qINE)

## 🤝 Contribuer
1. Fork le repo.
2. Créez une branche (`git checkout -b feature/ton-apport`).
3. Committez vos changements (`git commit -m "Ajout de X"`).
4. Poussez (`git push origin feature/ton-apport`).
5. Ouvrez une Pull Request.

## 📜 Licence
MIT License – voir [LICENSE](LICENSE).

## 📬 Contact
- **Auteur** : Ludovic Marchetti  
- **Email** : contact@datahootcome.fr  
- **GitHub** : [Ludovic-M-DAN](https://github.com/Ludovic-M-DAN)  
- **LinkedIn** : [L-Marchetti](https://www.linkedin.com/in/l-marchetti/)
