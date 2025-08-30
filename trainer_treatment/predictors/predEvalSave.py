# Importation des libraires nécessaires
import logging
from sklearn.metrics import accuracy_score, recall_score

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== EVAUATION ======
def evaluate_metrics(y_true,y_pred) :
    accuracy = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred, average="weighted")
    return accuracy, recall

# ====== PREDICTION + EVALUATION ======
def evaluate_predict(x_test, y_test, rf_model):
    try:
        # Stockage
        results ={}
        
        # Predict + Evaluate
        for name, content in rf_model.items():
            # Prediction
            y_pred = content.predict(x_test)
            logger.info("✅ Prediction done")
            # Evaluation
            accuracy, recall = evaluate_metrics(y_test, y_pred)
            logger.info("✅ Evaluation done")
            
            # Metrics
            results[name] = {
                "model": content, 
                "metrics" :{
                    "accuracy": accuracy, 
                    "recall": recall
                }
            }
        logger.info("✅ Prédiction + Evaluation")
        
        return results
    except Exception as e:
        logger.error(f"Erreur :{str(e)}")
        logger.exception("Stack trace : ")