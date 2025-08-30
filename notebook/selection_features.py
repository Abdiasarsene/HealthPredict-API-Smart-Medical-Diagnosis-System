# Importation des libriaires nécessaires
import os
# Gestion des warnings silencieux de Tensorflow 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import eli5
import shap
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from category_encoders import CatBoostEncoder
from sklearn.feature_selection import VarianceThreshold, chi2, RFE, SelectKBest
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, LabelEncoder, MinMaxScaler
from eli5.sklearn import PermutationImportance
from sklearn.compose import ColumnTransformer

# ====== LOGGING =======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== CHARGEMENT DU JEU DE DONNEES ======
data_path = r"D:\Projects\IT\Dara Science\HealthPredict - API\data\clinic_data.xlsx"
data = pd.read_excel(data_path)
logger.info("✅✅ Jeu de données chargé")

# ====== FEATURES + LABEL ======
x = data.drop(columns=["Diagnostique","Traitement"])
y = LabelEncoder().fit_transform(data["Diagnostique"])

# ====== DIVISION DES DONNEES EN ENTRAINEMENT ET DE TEST ======
x_train, x_test, y_train, y_test =train_test_split(x,y, test_size=0.2, random_state=42)

# ====== SEPARATION DES FEATURES NUMERIQUES ET CATEGORIELLES ======
num_cols = x_train.select_dtypes(include=['int64','float64']).columns.tolist()
cat_cols = x_train.select_dtypes(include=['object']).columns.tolist()

# ====== PRETRAITEMENT ======
num_transformed = Pipeline([
    ('impute', SimpleImputer(strategy='median')),
    ('sclaer', RobustScaler()),
    ('variance_selector', VarianceThreshold(threshold=0.1))
])

cat_tranformed = Pipeline([
    ('impute', SimpleImputer(strategy='most_frequent')),
    ('encoder', CatBoostEncoder()),
    ('scaler', MinMaxScaler()),
    ('chi2_selector', SelectKBest(score_func=chi2, k='all'))
])

preprocessor = ColumnTransformer([
    ('num', num_transformed, num_cols),
    ('cat', cat_tranformed, cat_cols)
])

x_train_preprocessed = preprocessor.fit_transform(x_train, y_train)
x_test_preprocessed = preprocessor.transform(x_test)

# Afichage des prints
logger.info("✅✅ Prétraitement fini")

# ===== RECUPERATION DES NOMS DE FEATURES TRANSFORMEES ======
def get_transformed_feature_names(preprocessor, num_transformed, cat_transformed):    
    num_selector = preprocessor.named_transformers_['num'].named_steps['variance_selector']
    cat_selector = preprocessor.named_transformers_["cat"].named_steps["chi2_selector"]
    
    selected_num = np.array(num_cols)[num_selector.get_support()]
    selected_cat = np.array(cat_cols)[cat_selector.get_support()]
    
    return list(selected_num) + list(selected_cat)

# Obtention des features
transformed_features = get_transformed_feature_names(preprocessor, num_cols, cat_cols)

# ====== APPLICATION DE RFE ======
rf = RandomForestClassifier(random_state=42, n_estimators=100)
model_rf = rf.fit(x_train_preprocessed, y_train)
rfe = RFE(estimator=model_rf, n_features_to_select=10)
rfe.fit(x_train_preprocessed, y_train)

# Récupération des features finales
final_features = np.array(transformed_features)[rfe.support_]

# Affichage des features finales retenues
logger.info("✅✅ Features finales retenues par RFE : %s", final_features)

# ====== APPLICATION DE LA PERMUTATION ======
x_train_rfe = rfe.transform(x_train_preprocessed)
x_test_rfe = rfe.transform(x_test_preprocessed)

rf.fit(x_train_rfe, y_train)
perm = PermutationImportance(rf, scoring='accuracy',random_state=42)
perm.fit(x_train_rfe, y_train)

# Affichage des importances
logging.info("\n🎯 Importance des features selon Permutation Importance")
eli5.show_weights(perm, feature_names=final_features.tolist())

# ====== CREATION DE LA NOUVELLE BASE DE DONNEES ======
features_selected = ['Temperature','Pulse', 'BloodPressure','SpO2','RespiratoryRate','BMI','FastingGlucose','Cholesterol','StressLevel','Fievre']

clinic_dataset = data[features_selected]
logger.info("✅✅Nouveau jeu de données collecté\n")
clinic_dataset.tail()

# Exportation des données
clinic_dataset.to_excel(r"D:\Projects\IT\Dara Science\HealthPredict - API\data\clinic_dataset.xlsx", index=False)
logger.info("\n✅✅ Nouveau jeu de données exporté")

# ====== APPLICATION DU SHAP ======
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(x_test_rfe)
shap.summary_plot(shap_values,x_test_rfe, feature_names=final_features)

# ====== EXPORTATION DES FEATURES SELECTIONNEES ET LEUR IMPORTANCE ======
pd.DataFrame({
    "feature": final_features,
    "importance": perm.feature_importances_
}).sort_values(by='importance', ascending=False).to_excel(r"D:\Projects\IT\Dara Science\HealthPredict - API\data\features_selected.xlsx")
logger.info("✅✅ Fichierb 'features_selected.xlsx' créé avec succès")
# Fin du script