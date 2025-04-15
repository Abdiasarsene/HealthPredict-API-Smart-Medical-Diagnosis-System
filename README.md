# HealthPredict

**HealthPredict** est une application basée sur l'intelligence artificielle qui analyse les données médicales pour prédire les maladies et suggérer des traitements appropriés. Ce projet utilise des techniques de machine learning (ML) et de deep learning (DL) pour offrir des prédictions de diagnostics ainsi que des suggestions de traitements adaptées à chaque patient.

## Table des matières

- [Objectifs du projet](#objectifs-du-projet)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Stack technologique](#stack-technologique)
- [Modèles développés](#modèles-développés)
- [Déploiement](#déploiement)
- [Installation](#installation)
- [Contribuer](#contribuer)
- [Contact](#contact)

## Objectifs du projet

- **Prédiction des maladies** : Utiliser des modèles supervisés comme Random Forest et Logistic Regression pour prédire les maladies en fonction des symptômes.
- **Proposition de traitements** : Suggérer des traitements adaptés selon les maladies identifiées.
- **Visualisation des données** : Explorer les tendances des données avec des graphiques interactifs.
- **Interface utilisateur intuitive** : Créer une interface simple pour les professionnels de santé afin de faciliter la consultation des résultats.

## Fonctionnalités principales

- **Importation des données** : Importer des fichiers Excel ou des données d'une base SQL pour analyser les données médicales.
- **Prédiction de la maladie** : Prédire la maladie en fonction des symptômes tels que la température, la pression artérielle, le pouls, etc.
- **Proposition de traitements** : Suggérer des traitements en fonction des maladies prédits.
- **Rapports détaillés** : Générer des rapports pour le suivi médical des patients.
- **Personnalisation des seuils diagnostiques** : Ajuster les paramètres diagnostiques pour personnaliser les prédictions.

## Stack technologique

- **Langage** : Python
- **Backend** : FastAPI
- **Frontend** : Streamlit
- **Machine Learning** : Scikit-learn (Random Forest, Logistic Regression, Gradient Boosting), TensorFlow/PyTorch pour Deep Learning
- **Visualisation** : Matplotlib, Plotly, Seaborn
- **Base de données** : PostgreSQL ou MySQL
- **Conteneurisation** : Docker pour déployer l'application en conteneur

## Modèles développés

Les principaux modèles utilisés dans le projet incluent :

1. **Random Forest Classifier** :
   - Utilisé pour prédire les maladies à partir des symptômes. Ce modèle permet une prise de décision robuste et précise, même avec des données bruitées.
   
2. **Logistic Regression** :
   - Utilisé pour prédire la probabilité de présence d'une maladie, notamment pour des problèmes de classification binaire.
   
3. **Gradient Boosting (XGBoost)** :
   - Utilisé pour optimiser la performance des prédictions, en combinant plusieurs modèles de manière itérative pour améliorer la précision.

4. **Réseaux de Neurones (Deep Learning)** :
   - Appliqué pour des prédictions plus complexes, où des relations non linéaires sont à explorer dans les données.

## Déploiement

### Lancer l'application en local avec Streamlit

1. Clone ce projet en utilisant la commande suivante :

   ```bash
   git clone https://github.com/tonutilisateur/HealthPredict.git
