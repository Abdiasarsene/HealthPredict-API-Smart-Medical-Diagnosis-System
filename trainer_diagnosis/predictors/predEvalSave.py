# === IMPORTS ===
import logging
from sklearn.metrics import accuracy_score, f1_score, recall_score

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== EVALUATION DES METRIQUES ======
def evaluate_metrics(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average= "weighted", zero_division=0)
    return accuracy, recall, f1

# ====== PREDICTION + EVALUATION ======
def predict_evaluate(x_test, y_test, best_models):
    try: 
        # Stockage dans un dictionnaire
        result = {}
        
        # Boucle
        for name, content in best_models.items():
            model = content["model"]
            # Prédiction
            y_pred = model.predict(x_test)
            logger.info("🚀 Prédiction faite")
            
            # Evaluation des perfomances
            accuracy, recall, f1 = evaluate_metrics(y_test, y_pred)
            logger.info("✅ Evaluation faite")
            
            # Encapsulation
            result[name] = {
                "model": model,
                "metrics" : {
                    "accuracy": accuracy,
                    "recall": recall,
                    "f1_score": f1
                }
            }
        logger.info("📊 Prédiction + Evaluation temrinée")
        return result
    except Exception as e: 
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")