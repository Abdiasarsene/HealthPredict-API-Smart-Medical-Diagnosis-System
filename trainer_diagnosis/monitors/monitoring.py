# Importation des librairies nécessaires
import mlflow
import logging
import bentoml

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== DATA LOADING METRICS ======
def log_data_overview(df):
    try: 
        mlflow.log_metric("n_row", df.shape[0])
        mlflow.log_metric("n_columns", df.shape[1])
        missing_total = df.isnull().sum().sum()
        mlflow.log_metric("missing_total", missing_total)
        logger.info("✅ Aperçu des données suivi")
    except Exception as e: 
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")

# ====== PREPROCESSING METRICS ======
def log_preprocessing_info(num_cols,cat_cols, text_cols=None):
    try:
        mlflow.log_metric("n_numeric_cols", len(num_cols))
        mlflow.log_metric("n_categorical", len(cat_cols))
        if text_cols:
            mlflow.log_metric("n_text_cols", len(text_cols))
        logger.info("✅ Prétraitement des données suivi")
    except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")

# ====== TRAINING METRICS ======
def log_training_info(model_name, duration_seconds):
    try:
        mlflow.log_param("models", model_name)
        mlflow.log_metric(f"{model_name}_time_duration", duration_seconds)
        logger.info("✅ Phase d'entrainement suivie avec MLflow")
    except Exception as e:
        logger.error(f"❌ Erreur : {str(e)}")
        logger.exception("Stack trace : ")

# ====== PREDICTION & EVALUATION ======
def log_prediction_info(evaluation_results):
    try:
        for name, content in evaluation_results.items():
            model = content["model"]
            metrics = content["metrics"]

            # ✅ Nested run pour chaque modèle
            with mlflow.start_run(run_name=f"{name}_eval", nested=True):
                # Logging Params
                mlflow.log_param("model_type", name)
                mlflow.log_params(model.get_params())
                logger.info(f"✅ Modèle {name} suivi avec Mlflow")
                
                # Logging Metrics
                for metric_name, value in metrics.items():
                    mlflow.log_metric(metric_name, value)
                logger.info("📊 Metrics suivies avec MLflow")
                
                # Logging Models
                mlflow.sklearn.log_model(model, name)
                logger.info(f"✅ Modèle {name} loggé avec MLflow")
                
                # Register model to MLflow Registry
                model_uri = f"runs:/{mlflow.active_run().info.run_id}/{name}"
                result = mlflow.register_model(model_uri=model_uri, name=name)
                
                client = mlflow.tracking.MlflowClient()
                client.transition_model_version_stage(
                    name=name,
                    version=result.version,
                    stage="Production",  # ⚠️ correction typo: "Prodcution" → "Production"
                    archive_existing_versions=True
                )
                logger.info(f"🚀 {name} promu en Production")
            
            # Save with BentoML
            bentoml.sklearn.save_model(name, model)
        logger.info("✍️ Modèles sauvegardés via MLflow et BentoML")
        
    except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")