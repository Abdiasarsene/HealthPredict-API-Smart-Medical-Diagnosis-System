# Chargement des bibliothèques nécessaires
import logging
import bentoml
import mlflow
import traceback

# ====== GESTION DES ERREURS AVEC LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== CHARGEMENT DES MODELES AVEC MLFLOW ======
# Diagnostique
def load_mlflow_model(path):
    try:
        logger.info(f" Chargement via MLflow depuis: {path}")
        model = mlflow.pyfunc.load_model(path)
        if model is None:
            raise RuntimeError("⚠️ Echec MLflow")
        return model
    except Exception as e: 
        logger.error(f"Erreur : {str(e)}")
        logger.debug(f"Traceback : {traceback.form_exc()}")

# Traitement
def load_treatment_model_mlflow(uri):
    return mlflow.sklearn.load_model(uri)

# ====== CHARGEMENT DES ERREURS AVEC BENTOML ======
# Diagnostique
def load_bentoml_model(tag):
    logger.info("🔄 Chargement via BentoML...")
    model = bentoml.sklearn.load_model(tag)
    if model is None: 
        raise RuntimeError("⚠️ Echec BentoML")

# Traitement
def load_treatment_model_bentoml(model_name):
    import bentoml
    return bentoml.sklearn.load_model(model_name)
