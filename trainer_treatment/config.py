# Importations des libraires nécessaires
from pydantic_settings import BaseSettings, SettingsConfigDict

# ====== CONFIGURATION ======
class Settings(BaseSettings):
    tracking_uri: str
    treatment_experiment: str
    dataset: str
    target_column: str

    model_config = SettingsConfigDict(
        env_file=".env.treat", 
        env_file_encoding="utf-8"
    )

settings = Settings()