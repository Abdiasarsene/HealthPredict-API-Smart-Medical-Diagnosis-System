# Importation des bibliothèques nécessaires
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import recall_score, f1_score, accuracy_score
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

# ====== Importer le jeu de données ======
data = pd.read_excel(r"D:\Projects\IT\Data Science & IA\Prediction_des_Maladies_et_Proposition_de_Traitement\datasets\clinic_data.xlsx")
print("Jeu de données importé ✅✅")

# ====== Prétraiter les données ======
print("Début du prétraitement✅✅")

# Séparer les features du target
x = data.drop(columns=['Diagnostique', 'Traitement'])
y = data["Diagnostique"]

# Encoder la cible
label = LabelEncoder()
y = label.fit_transform(y)

# Diviser les données en training et test
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2)

# Détecter les types de données
num_col = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_col = data.select_dtypes(include=["object"]).columns.difference(['Traitement', 'Diagnostique']).tolist()

# Prétraitement des données
num_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
    ('scaler', MinMaxScaler())
])

cat_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('oneencoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
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

# ====== Entraînement et Prédiction ======
print("Début de l'entraînement et de la prédiction ✅✅")

# Modèles à entraîner
models = {
    'logistic': LogisticRegression(max_iter=1000, solver='liblinear', class_weight="balanced"),
    'random_forest': RandomForestClassifier(),
    'xgboost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
}

# Hyperparamètres pour RandomizedSearchCV
param_dist = {
    "logistic": {
        "classifier__C": [0.1, 1, 10],
        "classifier__penalty": ["l1", "l2"]
    },
    "random_forest": {
        "classifier__n_estimators": [100, 200, 300],
        "classifier__max_depth": [3, 6, 10],
        "classifier__min_samples_split": [2, 5, 10]
    },
    "xgboost": {
        "classifier__learning_rate": [0.01, 0.05, 0.1, 0.2],
        "classifier__n_estimators": [100, 200, 300],
        "classifier__max_depth": [3, 6, 10],
        "classifier__subsample": [0.7, 0.8, 0.9],
        "classifier__colsample_bytree": [0.7, 0.8, 1],
        "classifier__gamma": [0, 0.1, 0.2]
    }
}

# Entraînement avec RandomizedSearchCV
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
best_models = {}

for name, model in models.items():
    print(f"\n🔍 Entraînement du modèle : {name}")
    
    pipe = Pipeline([
        ('preprocessing', preprocessor),
        ('classifier', model)
    ])
    
    random_search = RandomizedSearchCV(
        pipe,
        param_distributions=param_dist[name],
        n_iter=20,
        cv=cv,
        n_jobs=-1,
        scoring='accuracy',
        random_state=42
    )
    
    random_search.fit(x_train, y_train)
    best_models[name] = random_search.best_estimator_

# ====== Fonction de Log dans MLflow ======
def mlflow_log(model, x_test, y_test, model_name):
    try:
        # Prédiction et calcul des métriques
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        rec = recall_score(y_test, y_pred, average='weighted')

        with mlflow.start_run(run_name=model_name):
            # Log des paramètres et des métriques
            mlflow.log_param('model_type', model_name)
            mlflow.log_params(model.get_params())
            mlflow.log_metric('accuracy', acc)
            mlflow.log_metric('f1_score', f1)
            mlflow.log_metric('recall', rec)
            
            # Log du modèle dans MLflow
            mlflow.sklearn.log_model(model, model_name)
            
            # Enregistrement dans le Model Registry
            model_uri = f"runs:/{mlflow.active_run().info.run_id}/{model_name}"
            result = mlflow.register_model(model_uri=model_uri, name=model_name)
            print(f'Model {model_name} enregistré dans le Model Registry avec succès ✅✅')
            
            # Promotion automatique en Production
            client = MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=result.version,
                stage="Production",  # Tu peux utiliser "Staging" si tu préfères
                archive_existing_versions=True
            )
        print(f"✅ {model_name} enregistré avec succès dans MLflow\n")
        
    except Exception as e:
        print(f"❌ Une erreur est survenue lors du logging du modèle {model_name} : {e}")

# Enregistrement des modèles dans MLflow
for name, best_model in best_models.items():
    mlflow_log(best_model, x_test, y_test, name)

print("🎯 Tous les modèles ont été entraînés et enregistrés avec succès dans MLflow ✅✅✅")
