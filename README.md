# HealthPredict 🏥⚕️

**HealthPredict** est une application IA de diagnostic médical qui prédit des maladies et propose des traitements en temps réel, basée sur des modèles de machine learning déployés via une API RESTful.

![VSCode Screenshot](./images/code_screenshot.png)  
*Code source de l'application dans VSCode*

## Fonctionnalités clés

- 🔍 **Diagnostic intelligent** : Prédiction de maladies à partir des symptômes
- 💊 **Proposition de traitements** : Recommandations personnalisées
- 📊 **Tracking des modèles** : Versionning avec MLflow
- 🐳 **Déploiement conteneurisé** : Architecture Dockerisée
- 🔌 **API RESTful** : Intégration facile avec d'autres systèmes

## Stack Technique

| Composant       | Technologies                          |
|-----------------|---------------------------------------|
| **Backend**     | Python 3.9, FastAPI                   |
| **ML Models**   | Scikit-learn, XGBoost                 |
| **Tracking**    | MLflow                               |
| **Frontend**    | Streamlit (optionnel)                |
| **Database**    | PostgreSQL                           |
| **Infra**       | Docker, Docker-Compose               |

![MLflow Dashboard](./images/mlflow_screenshot.png)  
*Suivi des expériences ML dans MLflow*

## Modèles Implementés

| Modèle               | Accuracy | Cas d'usage                  |
|----------------------|----------|------------------------------|
| Random Forest        | 92%      | Diagnostics généraux         |
| XGBoost              | 94%      | Prédictions complexes        |
| Regression Logistique| 89%      | Diagnostics binaires         |
| SVM                  | 90%      | Cas marginaux                |

## Architecture
