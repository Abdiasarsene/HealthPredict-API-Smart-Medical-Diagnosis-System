# Importation des bibliotèqus utiles
import logging
import warnings
import numpy as np 
import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from scipy.stats.mstats import winsorize
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer


# ====== GESTION DES AVERTISSEMENTS EN MODE SILENCIEUX ======
warnings.filterwarnings("ignore")

# ====== GESTION DES COLONNES ======
def identify_columns(df: pd.DataFrame, label_col: str = "Diagnostique", drop_cols : list = ["Traitement"]):
    df = df.drop(columns=drop_cols)
    X = df.drop(columns= label_col)
    y = df[label_col]
    num_col = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_col = X.select_dtypes(include=["object"]).columns.tolist()
    return X,y, num_col, cat_col

# ====== GESTION DES VALEURS ABERRANTES ======
def winsorize_transform(X):
    X_winsorized = np.copy(X)
    for i in range(X.shape[1]) :
        X_winsorized[:, i]= winsorize(X[:,i], limits=[0.05,0.05])
    return X_winsorized

# ====== PIPELINE COMPLET DE FEATURES ======
def build_preprocessing_pipeline(num_col, cat_col):
    num_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="constant", fill_value=-1)),
        ("outlier", FunctionTransformer(winsorize_transform)),
        ("scaler", MinMaxScaler())
    ])
    
    cat_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="constant", fill_value="missing")),
        ("oneencoder", OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ("num", num_pipeline, num_col),
        ("cat", cat_pipeline, cat_col)
    ])
    return preprocessor


