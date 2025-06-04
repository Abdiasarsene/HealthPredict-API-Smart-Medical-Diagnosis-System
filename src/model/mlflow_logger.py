# === IMPORTS ===
import os
import mlflow
import logging
import warnings
import mlflow.sklearn
from src.model.config_ml import settings
from mlflow.tracking import MlflowClient
from sklearn.metrics import accuracy_score, f1_score, recall_score

# === WARNINGS SILENCIEUX ===
warnings.filterwarnings("all")

# === LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === UTILS : Créer ou récupérer l'ID de l'expérience ===
def get_or_create_experiment_id(experiment_name: str) -> str:
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is not None:
        return experiment.experiment_id
    else:
        return mlflow.create_experiment(experiment_name)

# === INITIALISATION DE L’EXPÉRIENCE MLFLOW ===
def init_mlflow_experiment():
    experiment_id = get_or_create_experiment_id(settings.MLFLOW_EXPERIMENT_NAME)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
    logger.info(f"✅✅ Expérience MLflow initialisée : {settings.MLFLOW_EXPERIMENT_NAME}")
    return experiment_id

# === LOGGING DU MODÈLE ===
def log_model_to_mlflow(model, x_test, y_test, model_name):
    try:
        # === Évaluation du modèle ===
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)

        # === Lancement du Run MLflow ===
        with mlflow.start_run(run_name=model_name):
            mlflow.log_param("model_type", model_name)

            # === Paramètres du modèle ===
            try:
                mlflow.log_params(model.named_steps['classifier'].get_params())
            except Exception as e:
                logger.warning(f"⚠️ Paramètres non loggés pour {model_name} : {e}")

            # === Métriques ===
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("recall", rec)

            # === Log du modèle ===
            try:
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path=model_name,
                    registered_model_name=settings.MLFLOW_MODEL_NAME
                )
            except Exception as e:
                logger.warning(f"❌ Erreur lors du log du modèle {model_name} : {e}")
                return  

            # === Enregistrement dans le Model Registry ===
            model_uri = f"runs:/{mlflow.active_run().info.run_id}/{model_name}"
            result = mlflow.register_model(model_uri=model_uri, name=settings.MLFLOW_MODEL_NAME)
            logger.info(f"✅✅ Modèle {model_name} enregistré dans le Model Registry")

            # === Passage à la production ===
            client = MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=result.version,
                stage="Production",
                archive_existing_versions=True
            )

        logger.info(f"🥅 Modèle {model_name} loggué avec succès dans MLflow\n")

    except Exception as e:
        logger.error(f"❌ Erreur lors du log du modèle {model_name} : {e}")
