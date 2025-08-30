# trainer_treatment/trainers/trainer.py
import logging
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== TRAINING ======
def train_model(x_train, y_train, preprocessor):
    try:
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            bootstrap=True,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
        model = Pipeline([
            ('preprocesing', preprocessor),
            ('random_forest', rf_model)
        ])
        
        model.fit(x_train, y_train)
        return model
    except Exception as e:
        logger.errro(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace : ")