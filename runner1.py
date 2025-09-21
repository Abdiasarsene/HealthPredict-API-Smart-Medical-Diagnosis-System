# Importation des bibliothèques
import time 
import mlflow
import logging
from trainer_diagnosis.config import settings
from trainer_diagnosis.loaders.data_loader import load_and_encode_dataset
from trainer_diagnosis.preprocessors.preprocessing import build_preprocessing_pipeline
from trainer_diagnosis.trainers.training import train_models
from trainer_diagnosis.predictors.predEvalSave import predict_evaluate
from trainer_diagnosis.monitors.monitoring import (
    log_data_overview,
    log_preprocessing_info,
    log_training_info, 
    log_prediction_info
)

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== MAIN PIPELINE ======
def main(): 
    try:
        # MLflow Initalized
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(settings.EXPERIMENT_NAME)
        
        with mlflow.start_run(run_name="DiseasePipeline"):
            
            # Step 1 : Data Loading & Target Encoding
            x_train, x_test, y_train, y_test,data= load_and_encode_dataset()
            log_data_overview(data)
            
            # Step 2 : Data Preprocessing
            preprocessor = build_preprocessing_pipeline(data)
            num_cols = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
            cat_cols = data.select_dtypes(include=['object']).columns.tolist()
            log_preprocessing_info(num_cols, cat_cols)
            
            # Step 3 : Models Training
            start_time = time.time()
            best_models = train_models(x_train, y_train, preprocessor)
            duration  = time.time() - start_time
            for model_name in best_models:
                log_training_info(model_name, duration)
            
            # Step 4 : Prediction + Evaluation + Loggin via MLflow and BentoML
            evauation_results = predict_evaluate(x_test, y_test, best_models)
            log_prediction_info(evauation_results)
            
        logger.info("🖥️ Pipeline Runned Sucessfully")
    except Exception as e:
        logger.error(f"❌ Pipeline Error : {str(e)}", exc_info=True)
        logger.exception("Stack trace : ")

# ====== MAIN BUTTOM ======
if __name__ == "__main__":
    main()