# Importation des libraires nécessaires
import bentoml
import mlflow
import logging

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== TRAINING METRICS ======*
def log_training_info(model_name, duration_seconds):
    try:
        mlflow.log_param("model", model_name)
        mlflow.log_metric(f"{model_name}_train_duration", duration_seconds)
        logger.info("✅ Phase d'entraînement suivie avec MLflow")
        
    except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace :  ")

# ===== PREDICTION & EVALUATION =====
def log_prediction_info(evaluation_results):
    try:
        for name, content in evaluation_results.items():
            model = content["model"]
            metrics = content["metrics"]
            
            with mlflow.start_run(run_name=f"{name}_eval", nested=True):
                # Logging Params
                mlflow.log_param("model_type", name)
                mlflow.log_params(model.get_params())
                logger.info(f"✅ Modèle {name} suivi avec MLflow")
                
                # Logging Metrics
                for metric_name, value in metrics.items():
                    mlflow.log_metric(metric_name, value)
                logger.info("📊 Metriques ")
                
                # Logging Models
                mlflow.sklearn.log_model(model,  name)
                logger.info("✅ Modèle Chargé")
            
            # Save du modèle avec BentoML
            bentoml.sklearn.save_model(name, model)
        logger.info("BentoML packagé")
            
    except Exception as e:
        logger.error(f"❌ Erreur : {str(e)}")
        logger.exception("Stack Trace :")