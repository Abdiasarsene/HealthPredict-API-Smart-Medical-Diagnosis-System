import pytest
from sklearn.utils.validation import check_is_fitted
from src.model.data_loader import load_dataset
from src.model.model_training import prepare_data, train_models
from src.model.mlflow_logger import log_model_to_mlflow
import numpy as np

def test_model_training_pipeline():
    df = load_dataset()
    x_train, x_test, y_train, y_test, num_col, cat_col, label = prepare_data(df)

    # Vérifie qu'on a bien des colonnes numériques et catégorielles
    assert len(num_col + cat_col) > 0

    best_models = train_models(x_train, y_train, num_col, cat_col)
    assert isinstance(best_models, dict)
    assert len(best_models) > 0

    for model_name, model in best_models.items():
        # Vérifie que le modèle est bien entraîné
        try:
            check_is_fitted(model)
        except Exception as e:
            pytest.fail(f"Le modèle {model_name} n'est pas entraîné correctement : {e}")
        
        # Prédiction de test
        y_pred = model.predict(x_test)
        assert isinstance(y_pred, np.ndarray)
        assert len(y_pred) == len(y_test)

        # Logging (vérifie juste que ça ne plante pas)
        log_model_to_mlflow(model, x_test, y_test, model_name)
