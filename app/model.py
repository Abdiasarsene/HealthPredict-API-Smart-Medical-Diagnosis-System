# Importation des bibliothèques nécessaires
import os
import mlflow
import warnings
import numpy as np
import pandas as pd
import mlflow.sklearn
from dotenv import load_dotenv
from sklearn.pipeline import Pipeline
from mlflow.tracking import MlflowClient
from sklearn.impute import SimpleImputer
from scipy.stats.mstats import winsorize
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder, FunctionTransformer

# ===== VARIABLE D'ENVIRONNEMENT ======
load_dotenv()

# ====== GESTION DES AVERTISSEMENTS EN MODE SILENCIEUX ======
warnings.filterwarnings('ignore')

# ====== IMPORTATION DU JEU DE DONNES ======
# Charger la variable d'environnement 
dataset_path = os.getenv("DATASET_PATH")

# Importer le jeu de données
data = pd.read_excel(dataset_path)
print("Jeu de données importé ✅✅")

# ====== PREPARATION DES DONNEES ======
x = data.drop(columns=['Diagnostique', 'Traitement'])
y = data["Diagnostique"]

# ====== ENCODAGE DU LABEL ======
label = LabelEncoder()
y = label.fit_transform(y)

# ====== DIVISION DES DONNEES EN ENTRAINEMENT ET DE TEST ======
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2)

# ====== SEPARATION DES TYPES DE DONNEES ======
features = data.drop(columns=['Traitement', 'Diagnostique'])
num_col = features.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_col = features.select_dtypes(include=["object"]).columns.tolist()

# ====== GESTION DES VALEURS ABERRANTES ======
def winsorize_transform(X):
    X_winsorized = np.copy(X)
    for i in range(X.shape[1]):
        X_winsorized[:,1] = winsorize(X[:,1], limits=[0.05,0.05])
    return  X_winsorized

# ====== PRETRAITEMENT DES DONNEES ======
# Colonne numerique
num_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
    ("winsorize", FunctionTransformer(winsorize_transform)),
    ('scaler', MinMaxScaler())
])

# Colonne catégorielle
cat_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('oneencoder', OneHotEncoder(handle_unknown='ignore'))
])

# ColumnTransformer 
preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_col),
        ('cat', cat_transformer, cat_col),
    ],
    remainder='drop'
)
print('Prétraitement terminé✅✅')

# ====== MODELES D'ENTRAPINEMENT ======
models = {
    'Logistic-Regression': LogisticRegression(max_iter=1000, solver='liblinear', class_weight="balanced"),
    'Random-Forest': RandomForestClassifier(random_state=42),
}

# ====== HYPERPARAMETRE AVEC RANDOMIZEDSEARCHGRID ======
param_dist = {
    "Logistic-Regression": {
        "classifier__C": [0.1, 1, 10],
        "classifier__penalty": ["l1", "l2"]
    },
    "Random-Forest": {
        "classifier__n_estimators": [100, 200, 300],
        "classifier__max_depth": [3, 6, 10],
        "classifier__min_samples_split": [2, 5, 10]
    },
}

# ====== ENTRAINEMENT DES MODELES ======
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
best_models = {}

for name, model in models.items():
    print(f"\n🔍 Entraînement du modèle : {name}")
    
    pipeline = Pipeline([
        ('preprocessing', preprocessor),
        ('classifier', model)
    ])
    
    random_search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_dist[name],
        n_iter=20,
        cv=cv,
        n_jobs=-1,
        scoring='accuracy',
        random_state=42
    )
    
    random_search.fit(x_train, y_train)
    best_models[name] = random_search.best_estimator_
print("Entraînement des modèles terminées ✅✅")

# ====== CREATION D'EXPERIENCE AVEC MLFLOW  ======
experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME")
mlflow.set_experiment(experiment_name)
print("Experience avec MLflow créée ✅✅")

# ====== FONCTION DE LOG DANS MLFLOW ======
def mlflow_log(model, x_test, y_test, model_name):
    try:
        # Prédiction et calcul des métriques
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted',zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted',zero_division=0)

        with mlflow.start_run(run_name=model_name):
            # Log des paramètres et des métriques
            mlflow.log_param('model_type', model_name)
            
            # log des paramètres
            try:
                mlflow.log_params(model.get_params())
            except Exception as e : 
                print(f"⚠️ Impossible de loguer les paramètres  pour {model_name}")
            
            # mlflow.log_params(model.get_params())
            mlflow.log_metric('accuracy', acc)
            mlflow.log_metric('f1_score', f1)
            mlflow.log_metric('recall', rec)
            
            # Log du modèle dans MLflow
            try: 
                mlflow.sklearn.log_model(model, model_name)
            except Exception as e : 
                print(f"⚠️ Erreur lors du log du modèle {model_name} : {e}")
            
            # Enregistrement dans le Model Registry
            model_uri = f"runs:/{mlflow.active_run().info.run_id}/{model_name}"
            result = mlflow.register_model(model_uri=model_uri, name=model_name)
            print(f'Model {model_name} enregistré dans le Model Registry avec succès ✅✅')
            
            # Promotion automatique en Production
            client = MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=result.version,
                stage="Production",  
                archive_existing_versions=True
            )
        print(f"✅ {model_name} enregistré avec succès dans MLflow\n")
        
    except Exception as e:
        print(f"❌ Une erreur est survenue lors du logging du modèle {model_name} : {e}")

# Enregistrement des modèles dans MLflow
for name, best_model in best_models.items():
    mlflow_log(best_model, x_test, y_test, name)

print("🎯 Tous les modèles ont été entraînés et enregistrés avec succès dans MLflow ✅✅✅")