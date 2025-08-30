# model.py
import logging
import mlflow
import time
from trainer_treatment.config import settings
from trainer_treatment.loaders.data_loader import load_and_encode
from trainer_treatment.preprocessors.preprocessing import get_preprocessing
from trainer_treatment.trainers.training import trainer
from trainer_treatment.predictors.predEvalSave import evaluate_predict
from trainer_treatment.monitors.monitor import log_training_info, log_prediction_info

# ======= LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== MAIN ACTION ====
def main():
    try:
        # MLflow Initialized
        mlflow.set_tracking_uri(settings.tracking_uri)
        mlflow.set_experiment(settings.treatment_experiment)
        with mlflow.start_run(run_name="TreatmentPipeline"):
            
            # Step 1 : Load and Split 
            x_train, x_test, y_train, y_test, data = load_and_encode()
            
            # Step 2 : Preprocessing
            preprocessor = get_preprocessing(data)
            
            # Step 3 : Model Training
            start_time = time.time()
            rf_model = trainer(x_train, y_train, preprocessor)
            duration = time.time() - start_time
            for  model_name in rf_model:
                log_training_info(model_name, duration)
            
            # Step 4 : Prediction + Evaluation + Save Models
            evaluate_result = evaluate_predict(x_test, y_test, rf_model)
            log_prediction_info(evaluate_result)
        logger.info("🔃 Pipeline Runned Succesfully")
    except Exception  as e:
        logger.error(f"❌ Pipeline Error : {str(e)}")
        logger.exception("Stack trace : ")

# ====== MAIN BUTTON =======
if __name__ == "__main__":
    main()