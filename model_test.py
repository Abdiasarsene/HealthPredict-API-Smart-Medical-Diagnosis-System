# Importation des librairies
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from scipy.stats import randint, uniform
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score
import mlflow
import mlflow.sklearn

# Importation de la base de données traitée
data_treated = pd.read_excel(r'D:\Projects\IT\Data Science & IA\Prediction_des_Maladies_et_Proposition_de_Traitement\explore\data\data_health_treated.xlsx')
print("Données importées avec succès ✅✅✅")

# Préparation des données
x = data_treated.drop(columns=['Diagnosis', 'Treatment'])
y = data_treated['Treatment']

# Normalisation
scaler = MinMaxScaler()
x_normalized = scaler.fit_transform(x)
print("Données normalisées avec succès ✅✅✅")

# Division en données d'entraînement et de test
SEED = 42
x_train, x_test, y_train, y_test = train_test_split(x_normalized, y, test_size=0.2, random_state=SEED)

# Régression Logistique
lr = LogisticRegression(random_state=SEED, class_weight='balanced')
lr_dist = {
    'C': uniform(0.01, 100),
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}
lr_gs = RandomizedSearchCV(
    estimator=lr,
    param_distributions=lr_dist,
    cv=5,
    n_jobs=-1,
    scoring='accuracy',
    random_state=SEED
)
lr_model = lr_gs.fit(x_train, y_train)
print('Régression Logistique terminée ✅✅✅')

# Forêt aléatoire et validation croisée
rf = RandomForestClassifier(random_state=SEED, class_weight='balanced')
rf_dist = {
    'n_estimators': randint(100, 800),
    'max_depth': randint(10, 30),
    'criterion': ["gini", "entropy"],
    'max_leaf_nodes': randint(10, 100)
}
rf_gs = RandomizedSearchCV(
    estimator=rf,
    param_distributions=rf_dist,
    cv=5,
    n_jobs=-1,
    scoring='accuracy',
    verbose=0
)
rf_model = rf_gs.fit(x_train, y_train)
print('Random Forest successful ✅✅✅')


# Gradient Boosting
gb = GradientBoostingClassifier(random_state=SEED)
gb_dist = {
    'n_estimators': randint(100, 500),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(2, 10),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 5)
}
gb_gs = RandomizedSearchCV(
    estimator=gb,
    param_distributions=gb_dist,
    scoring='accuracy',
    cv=5,
    n_jobs=-1,
    random_state=SEED
)
gb_model = gb_gs.fit(x_train, y_train)
print('Gradient Boosting terminé ✅✅✅')

# Configuration MLflow
mlflow.set_experiment('First Model')

# Fonction de log dans MLflow
def mlflow_log(model, x_test, y_test, model_name):
    try:
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        rec = recall_score(y_test, y_pred, average='weighted')

        with mlflow.start_run(run_name=model_name):
            mlflow.log_param('model_type', model_name)
            mlflow.log_params(model.best_params_)
            mlflow.log_metric('accuracy', acc)
            mlflow.log_metric('f1_score', f1)
            mlflow.log_metric('recall', rec)
            mlflow.sklearn.log_model(model.best_estimator_, model_name)

        print(f"\n⚙️ Performance {model_name}:")
        print(f"✅ Best params: {model.best_params_}")
        print(f"✅ Accuracy = {acc:.4f}")
        print(f"✅ F1 Score = {f1:.4f}")
        print(f"✅ Recall = {rec:.4f}")
        print(f"✅ {model_name} enregistré avec succès dans MLflow\n")
        
    except Exception as e:
        print(f"❌ Une erreur est survenue lors du logging du modèle {model_name} : {e}")

# Enregistrement dans MLflow
mlflow_log(lr_model, x_test, y_test, "Logistic_Regression")
mlflow_log(rf_model, x_test, y_test, "Random_Forest")
mlflow_log(gb_model, x_test, y_test, "Gradient_Boosting")

print("🎯 Tous les modèles ont été entraînés et enregistrés avec succès dans MLflow ✅✅✅")
