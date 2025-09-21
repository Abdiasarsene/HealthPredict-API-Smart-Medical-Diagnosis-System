# cat_cols/extractor_cols.py
import os
import json
import logging 
import pandas as pd
from dotenv import load_dotenv

# ====== INTIALISATION ======
load_dotenv(dotenv_path=".env.treat", override=True)

# ======= LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======== EXTRACT COLS FUNCTION ======
def cat_cols_function():
    try:
        # Jeu de données 
        dataset = os.getenv("DATASET")
        if dataset is None:
            raise FileNotFoundError("❌ Fichier Pas Trouvé")
        
        # Import data
        data = pd.read_excel(dataset)
        logger.info("✅ Data Loaded")
        
        # Extract categoricals and numericals cols
        cat_cols = data.select_dtypes(include=["object"]).columns.tolist()
        num_cols = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
        
        # Single modalities for cat cols
        categoricals = {
            col : data[col].dropna().unique().tolist()
            for col in cat_cols
        }
        logger.info("✅ Modalités extraites dans les colonnes catégorielles")
        
        # Min/max values for num cols
        numericals = {
            col :{
                "min" : data[col].min(),
                "max" : data[col].max()
            }
            for col in num_cols
        }
        logger.info("✅ Min & Max extraits dans chaque colonne numériques")
        
        # Dico that packages all
        extracted_cols = {
            "categoricals" : categoricals,
            "numericals" : numericals
        }
        
        # Download the file
        cols_json = os.getenv("COLS_JSON")
        with open(cols_json, "w", encoding="utf-8") as f:
            json.dump(extracted_cols, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ Extraction des modalités uniques : {cols_json}")
    
    except Exception as e:
        logger.error(f"❌ Erreur Détectée : {str(e)}")
        logger.exception("⚠️ Stack Trace : ")

# ====== BOUTON PRINCIPAL ======
if __name__ == "__main__" :
    cat_cols_function()