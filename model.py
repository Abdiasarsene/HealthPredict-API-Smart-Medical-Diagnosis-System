# Importation des bibliothèques 
import logging
import warnings
from src.model.data_loader import load_dataset
from src.model.preprocessing import identify_columns, build_preprocessing_pipeline
from src.model.model_training import prepare_data, train_models
from src.model.mlflow_logger import init_mlflow_experiment, log_model_to_mlflow

# ====== GESTION DES AVERTISSEMENTS EN MODE SILENCIEUX ======
warnings.filterwarnings("ignore")

# ====== LOGGIGNG =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(): 
    # Etape 1 : Chargement des données
    df = load_dataset()
    logger.info("✅ Jeu de données")
    
    # Etape 2 : Initialisation de l'expérience MLflow
    init_mlflow_experiment()
    logger.info("✅ Expérience MLflow créée")
    
    # Etape 3 : Préparation des données
    x_train, x_test, y_train, y_test, num_col, cat_col, label_encoder = prepare_data(df)
    
    # Etape 4 : Entraînement des modèles
    best_models = train_models(x_train, y_train, num_col, cat_col)
    
    # Etape 5 : Log des modèles entraînés + monitoring
    for model_name, model in best_models.items():
        log_model_to_mlflow(model, x_test, y_test, model_name)

if __name__ == "__main__":
    main()