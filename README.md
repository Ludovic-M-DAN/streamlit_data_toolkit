# <img src="logo.png" alt="Logo" width="40" style="vertical-align: text-bottom;"/> Data Toolkit

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

**Data Toolkit** est une application interactive Streamlit qui simplifie l'exploration, l'analyse et le traitement de fichiers CSV ou Excel. Elle s'adresse aux data scientists, analystes ou toute personne souhaitant explorer ses données via une interface intuitive.

## 🎯 Motivation
L’objectif est de centraliser les étapes courantes de l’analyse de données (souvent dispersées dans des scripts ou notebooks) dans un outil convivial, pour gagner du temps et se concentrer sur l’interprétation des résultats.

## 🚀 Fonctionnalités

### Basiques
- **Chargement** : Import de fichiers CSV/Excel (jusqu’à 5 Go) avec séparateur personnalisé.
- **Prévisualisation** : Aperçu des 5 premières lignes avant chargement complet.
- **Informations de base** : Dimensions, types de colonnes, valeurs manquantes, taille en mémoire.
- **Traitement** : Échantillonnage (aléatoire, premières/dernières N lignes) avec export.

### Avancées
- **EDA+** : Statistiques descriptives, visualisations (histogrammes, corrélations, boîtes à moustaches, valeurs manquantes).
- **Personnalisation** : Choix des colonnes et des analyses.
- **Logs** : Gestion des erreurs dans `app.log`.

## 📂 Structure du Repository
```
streamlit_data_toolkit/
├── data/                     # Datasets d’exemple
├── docs/                     # Documentation détaillée
│   ├── user_guide.md
│   └── api_reference.md
├── src/                      # Code source
│   ├── config.py
│   ├── data_loader.py
│   ├── eda.py
│   ├── eda_advanced.py
│   └── utils.py
├── tests/                    # Tests unitaires
├── .gitignore
├── app.py                    # Application principale
├── LICENSE                   # MIT License
├── logo.png                  # Logo
├── README.md
└── requirements.txt          # Dépendances
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
source venv/bin/activate  # Windows : venv\Scripts\activate
```

3. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

4. **Lancer l’app** :
```bash
streamlit run app.py
```

Ouvre http://localhost:8501 dans ton navigateur.

## 📖 Documentation
- **Guide utilisateur** : Instructions détaillées avec captures d’écran.
- **Référence API** : Détails des fonctions.

## 📸 Captures d’écran
(en cours)

## 🤝 Contribuer
1. Fork le repo.
2. Crée une branche (`git checkout -b feature/ton-apport`).
3. Commit tes changements (`git commit -m "Ajout de X"`).
4. Push (`git push origin feature/ton-apport`).
5. Ouvre une Pull Request.

## 📜 Licence
MIT License – voir [LICENSE](LICENSE).

## 📬 Contact
- **Auteur** : Ludovic Marchetti  
- **Email** : contact@datahootcome.fr  
- **GitHub** : [Ludovic-M-DAN](https://github.com/Ludovic-M-DAN)