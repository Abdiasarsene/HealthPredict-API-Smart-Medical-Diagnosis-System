# Importation de la base de données
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
from sklearn.metrics import recall_score, f1_score, confusion_matrix, accuracy_score
import mlflow
import mlflow.sklearn
import mlflow.xgboost

# ====== Importer le jeu de données ======
data = pd.read_excel(r"D:\Projects\IT\Data Science & IA\Prediction_des_Maladies_et_Proposition_de_Traitement\datasets\clinic_data.xlsx")
print("Jeu de données importé ✅✅")

# ====== Prétraiter les données ======
print("Début du prétraitement✅✅")

# Séparer des features/Target
x = data.drop(columns=['Diagnostique','Traitement'])
y = data["Diagnostique"]

# Encoder du Target 
label = LabelEncoder()
y = label.fit_transform(y)

# Diviser les données en entraînement et de test ===
x_train, x_test, y_train, y_test = train_test_split(x,y, random_state=42, test_size=0.2)

# Détecter automatiquement les types de données ===
num_col = data.select_dtypes(include=['int64','float64']).columns.tolist()
cat_col = data.select_dtypes(include=["object"]).columns.difference(['Traitement','Diagnostique']).tolist()

# Préprocesseurs
num_transformer =Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
    ('scaler', MinMaxScaler())
])

cat_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('oneencoder', OneHotEncoder(sparse_output= False, handle_unknown='ignore'))
])

# ColumnTransformer général
preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_col),
        ('cat',cat_transformer,cat_col),
    ],
    remainder='drop'
)
print('Prétraitement terminé✅✅')

# ====== Entraînement et Prédiction ======
print("Debut d'entraînement et de prédiction ✅✅")

# Modèles à entraîner
models = {
    'logistic': LogisticRegression(max_iter=1000, solver='liblinear',class_weight="balanced"),
    'xgboost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
}

# Grilles d'hyperparamètres
param_dist = {
    "logistic": {
        "classifier__C": [0.1, 1, 10],
        "classifier__penalty": ["l1", "l2"]
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
        n_iter=20,  # tu peux ajuster selon ton temps de calcul
        cv=cv,
        n_jobs=-1,
        scoring='accuracy',
        random_state=42
    )
    
    random_search.fit(x_train, y_train)
    best_model = random_search.best_estimator_
    best_models[name] = best_model
    
    # ====== Évaluation ======
    y_pred = best_model.predict(x_test)
    
    acc = accuracy_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    cm = confusion_matrix(y_test, y_pred)
    
    # Afficher les résultats
    print(f"✅ {name.upper()} - Accuracy : {acc:.3f} | Recall : {rec:.3f} | F1-score : {f1:.3f}")
    print(f"Meilleurs hyperparamètres : {random_search.best_params_}")
    print(f"Confusion Matrix : \n{cm}")
print("Entraînement et prédiction terminés ✅✅")

# ====== Enrégistrement dans Mlflow ======
print("Debut d'entraînement dans MLflow ✅✅")

# Fonction simplifiée pour loguer le modèle et les métriques
def log_model_to_mlflow(model, model_name, accuracy, recall, stage):
    with mlflow.start_run():
        # Enregistrer le modèle avec MLflow
        if isinstance(model, LogisticRegression):
            mlflow.sklearn.log_model(model, model_name)
        elif isinstance(model, XGBClassifier):
            mlflow.xgboost.log_model(model, model_name)
        
        # Enregistrer les métriques
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("recall", recall)

        # Enregistrer le modèle dans le Model Registry avec une étiquette de "Stage" ou "Production"
        model_uri = f"runs:/{mlflow.active_run().info.run_id}/{model_name}"
        mlflow.register_model(model_uri, model_name)
        
        # Transitionner le modèle dans le stage
        model_versions = mlflow.list_registered_models()
        latest_version = max([version.version for version in model_versions if version.name == model_name], default=None)
        
        if latest_version:
            mlflow.transition_model_version_stage(
                name=model_name,
                version=latest_version,
                stage=stage
            )

# Enregistrer les modèles et leurs résultats
for name, best_model in best_models.items():
    # Calcul des métriques
    accuracy = accuracy_score(y_test, best_model.predict(x_test))
    recall = recall_score(y_test, best_model.predict(x_test), average='macro')

    # Enregistrer le modèle avec le stage approprié
    if name == 'logistic':
        log_model_to_mlflow(best_model, name, accuracy, recall, stage="Staging")
    elif name == 'xgboost':
        log_model_to_mlflow(best_model, name, accuracy, recall, stage="Production")


print('Enregistrement dans MLflow terminé ✅✅')