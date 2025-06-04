# Importation des bibliothèques
import logging
import warnings
import numpy as np
from src.model.config_ml import settings
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from src.model.preprocessing import build_preprocessing_pipeline, identify_columns
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, train_test_split

# ====== GESTION DES AVERTISSEMENTS EN MODE SILENCIEUX ======
warnings.filterwarnings("ignore")

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== PREPARATION DES DONNEES ======
def prepare_data(data):
    X, y, num_col, cat_col = identify_columns(data)
    
    # Encodage de la cible 
    label  = LabelEncoder()
    y_encoded = label.fit_transform(y)
    
    # Division des données en entraînement et de test
    x_train, x_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    
    return x_train, x_test, y_train, y_test, num_col, cat_col, label

# ====== DEFINITION DES MODELES  ET HYPERPARAMETRES ======
def get_model_and_param():
    models = {
        "Logistic-Regression": LogisticRegression(max_iter=1000, solver="liblinear", class_weight="balanced"),
        "Random-Forest":RandomForestClassifier(random_state=42)
    }
    
    # Optimisation des hyperparamètres
    param_dist = {
        "Logistic-Regression":{
            "classifier__C":[0.1,1,10],
            "classifier__penalty": ["l1","l2"]
        },
        "Random-Forest":{
            "classifier__n_estimators": [100,200,300],
            "classifier__max_depth": [3,6,10],
            "classifier__min_samples_split": [2,5,10]
        }
    }
    
    return models, param_dist

# ====== ENTRAINEMENT AVEC RANDOMIZEDSEARCHGRID ======
def train_models(x_train, y_train, num_col, cat_col):
    models, param_dist = get_model_and_param()
    best_models = {}
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    for name, model in models.items():
        preprocessor = build_preprocessing_pipeline(num_col, cat_col)
        pipeline = Pipeline([
            ("preprocessing", preprocessor),
            ("classifier", model)
        ])
        
        search = RandomizedSearchCV(
            pipeline,
            param_distributions=param_dist[name],
            n_iter=20,
            cv=cv,
            n_jobs=-1,
            scoring="accuracy",
            random_state=42
        )
        search.fit(x_train, y_train)
        best_models[name] = search.best_estimator_
    logger.info("✅✅ Entraînement terminé pour tous les modèles : {list(best_model.keys())}")
    
    return best_models