# Importation des libraires nécessaires
import logging
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

# ====== ENTRINEMENT ======
def trainer(x_train, y_train, preprocessor):
    try:
        # Model
        model ={
            "random_forest" : RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                class_weight="balanced",
                min_samples_split=10,
                min_samples_leaf=4
            )
        }
        
        # Dico pour garder le model
        rf_model = {}
        
        # Entraînement + Sauvegarde
        for name, content in model.items():
            
            # Pipeline
            pipeline = Pipeline([
                ('preprocessing', preprocessor),
                ("model", content)
            ])
            
            # Entraînement
            pipeline.fit(x_train, y_train)
            
            # Sauvegarde
            rf_model[name] = pipeline
            logger.info(f"✅ {name} trained")
            print(type(rf_model))
        return rf_model
    except Exception as e : 
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace :")