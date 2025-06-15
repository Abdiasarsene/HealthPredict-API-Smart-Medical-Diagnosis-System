# 🎯 HealthPredict — AI-Powered Disease and Treatment Prediction API

HealthPredict est une API robuste et modulaire, conçue pour prédire automatiquement des diagnostics médicaux et recommander des traitements adaptés à partir de données cliniques.
Ce projet illustre une intégration avancée de pipelines ML avec MLflow et BentoML, assurant un déploiement scalable et un fallback intelligent entre modèles.

---

## 🧠 Objectifs du Projet

* Automatiser la prédiction fiable de diagnostics à partir de données physiologiques et cliniques
* Proposer un traitement médical cohérent basé sur le diagnostic prédit
* Implémenter une gestion robuste des modèles avec fallback entre MLflow et BentoML
* Offrir un pipeline prêt pour la production avec logs, gestion des erreurs et tests
* Supporter un workflow asynchrone avec FastAPI pour la scalabilité

---

## 🧰 Stack Technique

| Domaine                  | Outils & Frameworks                |
| ------------------------ | ---------------------------------- |
| Modélisation ML          | Scikit-learn, CatBoost, Pipelines  |
| Encodage & Prétraitement | CatBoostEncoder (feature encoding) |
| Suivi Expériences        | MLflow (Tracking & Registry)       |
| Packaging Modèle         | BentoML                            |
| API Serving              | FastAPI                            |
| Monitoring               | Prometheus + Grafana |
| Tests                    | Pytest                             |
| Containerisation         | Docker, Docker Compose             |
| Orchestration            | asyncio (startup event fallback)   |
| CI/CD                    | Jenkins, Makefile                  | 
---

## 🏗️ Architecture Modulaire

```
healthpredict/
│
├── app/                  # FastAPI app for serving predictions (BentoML runtime)
├── train\_pipeline/       # Feature engineering, training, inference, model saving
├── retrain/              # (WIP) Scheduled retraining logic with Celery + Beat
├── notebook/             # EDA and feature selection experiments
├── docker/               # Custom Dockerfiles
├── tests/                # Unit/integration test suites
├── Jenkinsfile           # CI/CD pipeline config
├── Makefile              # Unified entrypoint for all tasks
├── dataset.dvc           # DVC-tracked dataset pointer
└── README.md
```

---

## 🔄 Workflow de Prédiction

1. **Chargement modèle en startup**

   * Priorité à MLflow avec timeout (10s)
   * En cas d’échec, fallback vers BentoML
   * Logs complets et gestion des erreurs critiques

2. **Validation des données via Pydantic**

   * Validation stricte des champs, encodage enum personnalisé
   * Gestion des alias pour faciliter l’intégration front-end

3. **Pipeline de prédiction combinée**

   * Modèle diagnostic : sortie int → mapping nom maladie
   * Modèle traitement : sortie int → mapping type traitement
   * Encodage intégré dans pipeline ML (pas d’encodage manuel côté API)

4. **Réponse API claire et documentée**

   * Diagnostic prédit + traitement recommandé
   * Statut & modèle utilisé pour auditabilité

---

## ⚙️ Meilleures Pratiques Intégrées

* Encapsulation claire des modèles & logique métier (`model_loader.py`, `predictor.py`)
* Gestion robuste des exceptions avec logs (`logging`, HTTPException)
* Modèle fallback pour haute disponibilité et tolérance aux pannes
* Typage strict & validation via Pydantic pour éviter erreurs en production
* Utilisation d’`asyncio` pour chargement asynchrone non bloquant
* Séparation claire entre logique API, prédiction & chargement modèle

---

## 🔒 Reproductibilité & Déploiement

* Environnements isolés avec Docker
* Suivi des versions de modèles via MLflow & BentoML
* Tests automatisés pour validation continue
* Documentation claire pour intégration & maintenance

---

## 📍 État actuel du projet

* ✅ Pipeline ML complet (diagnostic + traitement)
* ✅ API FastAPI robuste avec fallback modèle
* ✅ Validation d’entrée complète via Pydantic
* ✅ Gestion d’erreurs et logs configurés
* 🔜 Ajout tests automatisés & monitoring API avancé

---

## 🔄 Réentrainement Continu (CT) (prévue)

Un module `retrain/` est prévu pour les mises à jour programmées des modèles utilisant **Celery + Beat**.  
Points clés :
- De nouvelles données déclenchent un pipeline programmé
- Le modèle ré-entraîné est **comparé** au modèle actuellement déployé.
- Le nouveau modèle n'est promu que s'il est plus performant que le modèle actuel.
- Sinon, le système conserve le modèle existant.

---

## 📊 Capacités de surveillance

Mesures déployées collectées en temps réel :
- Latence de l'API, santé, temps de fonctionnement (Prometheus)
- Nombre de requêtes, taux d'erreur
- Détection des dérives sur les flux de données entrants
- Contrôles de la qualité des données sur les entrées
  
---

## ✅ Pipeline CI/CD

Tous les composants sont intégrés dans un `Jenkinsfile` de niveau production :
- ✅ Tests unitaires
- ✅ Lint checks
- ✅ Construire une image Docker
- ✅ Déclencher le packaging MLflow ou BentoML
- Phase de déploiement optionnelle
- Notifications Slack/Webhook (optionnel)

---

## ⚙️ Commandes Makefile

```bash
make train       # Train and log with MLflow
make test        # Run test suite
make run         # Launch BentoML API server
make deploy      # Build + push containers
make monitoring  # Start Prometheus + Grafana stack
make format      # Run flake8 or ruff
````
---

## 🔗 À propos

Construit par **Abdias Arsène**, Consultant IT en IA & MLOps
Focalisé sur des solutions ML réelles et inter-industrielles (Santé, Humanitaire, Finance, Logistique artistique)

> *“Un code propre, robuste et maintenable est la clé pour transformer une idée en solution durable.”*

---
