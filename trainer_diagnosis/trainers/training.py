# Importation des bibliothèques
import logging
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== DEFINITION DES MODELES  ET HYPERPARAMETRES ======
def train_models(x_train, y_train, preprocessor):
    try:
        models = {
            "logistic-regression": LogisticRegression(max_iter=1000, solver="liblinear", class_weight="balanced"),
            "random-forest":RandomForestClassifier(random_state=42)
        }
        
        # Optimisation des hyperparamètres
        param_dist = {
            "logistic-regression":{
                "classifier__C":[0.1,1,10],
                "classifier__penalty": ["l1","l2"]
            },
            "random-forest":{
                "classifier__n_estimators": [100,200,300],
                "classifier__max_depth": [3,6,10],
                "classifier__min_samples_split": [2,5,10]
            }
        }
        
        best_models = {}
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for name, model in models.items():
            logger.info(f"\n Entraînement du modèle : {name}")
            
            pipeline = Pipeline([
                ("preprocessing", preprocessor),
                ("classifier", model)
            ])
            
            search = RandomizedSearchCV(
                pipeline,
                param_distributions=param_dist[name],
                n_iter=10   ,
                cv=cv,
                n_jobs=-1,
                scoring="accuracy",
                random_state=42
            )
            
            search.fit(x_train, y_train)
            best_models[name] = {
                "model": search.best_estimator_,
                "params": search.best_params_,
                "cv_results": search.cv_results_,
                "best_score": search.best_score_
            }

        logger.info("✅✅ Entraînement terminé pour tous les modèles")
        return best_models
    
    except Exception as e: 
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")
        raise e