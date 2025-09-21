# app/core/data_transformer.py  
import logging
import pandas as pd 

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== TRANSFORME LES ENTREES EN DATAFRAME 2D ======
def normalize_input(payload):
    try:
        # Already DataFrame
        if isinstance(payload, pd.DataFrame):
            return payload.reset_index(drop=True)
        
        # List of Dicts
        if isinstance(payload, list) and all(isinstance(x, dict) for x in payload) :
            return pd.DataFrame(payload)
        
        # Dict or Series dict
        if  isinstance(payload, dict):
            clean = {}
            for k, v in payload.items():
                if isinstance(v, pd.Series):
                    clean[k] = v.iloc[0]
                else:
                    clean[k] = v
            return pd.DataFrame([clean])
        
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("⚠️ Stack trace : ")
        raise ValueError(f" Unsupported Format : {type(payload)}")
