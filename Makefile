.PHONY: schema train format mlflow app radon bandit mypy features

# Dossier
TEST_DIR=tests
NOTEBOOK_DIR = notebook
DISEASE_DIR = trainer_diagnosis
TREATMENT_DIR = trainer_treatment
APP_DIR = app

# ====== DEFAULT PIPELINE ======
default: radon bandit format mypy
	@echo "Default Pipeline Done"

# ====== LANCEMENT DU TEST DE L'API ======
schema:
	@echo "Valider les données d'entrée"
	@python $(TEST_DIR)/schema_test.py

# ======= LANCEMENT DU PIPELINE DU MODELE ======
train:
	@echo "Lancement du pipeline entrainement"
	@python runner.py

# ======= FORMATAGE + LINTING ======
format:
	@echo "Formatage + linting"
	@ruff check . --fix

# ====== LANCEMENT LA CONNEXION MLFLOW ======
mlflow:  
	@echo "Connexion a MLflow"
	@mlflow ui 

# ====== LANCEMENT DE L'API ======
app:
	@echo "Lancement de HealthPredict API"
	@uvicorn main:app --reload --port 8000 --workers 1

# ====== ANALYSE CYCLO =======
radon:
	@echo "Analyse Cyclo"
	@radon mi $(TEST_DIR)/ $(DISEASE_DIR)/ $(TREATMENT_DIR)/ $(APP_DIR)/ -s

# ====== ANALYSE DU CODE SOURCE ======
bandit:
	@echo "Analyse du code"
	@bandit -r $(TEST_DIR)/ $(DISEASE_DIR)/ $(TREATMENT_DIR)/ $(APP_DIR)/ -ll

# ====== MYPY ======
mypy:
	@echo "MyPy"
	@mypy --config mypy.ini

# ====== AFFICHAGE DES FEATURES RETENUES =====
features:
	@echo "Features finales retenues"
	@py $(NOTEBOOK)/selection_features.py

# ====== MODELS TREATMENT =====
model:
	@echo "Modele de traitement"
	@python model.py

# ====== BENTOML ======
bentoml:
	@echo "Check des modeles sur BentoML"
	@python -m bentoml models list