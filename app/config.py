# app/config.py
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import ValidationError, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Load specific env file 
force = os.getenv("FORCE_ENV_MODE")
env_file = None

if force == "docker" or Path("/.dockerenv").exists():
    env_file = ".env.docker"
elif force == "local":
    env_file = ".env.local"

if env_file and Path(env_file).exists():
    load_dotenv(dotenv_path=env_file, override=True)
else:
    env_file = ".env.local"

# 2. BaseSettings config
class Settings(BaseSettings):
    # Settings 
    env_mode: str
    tracking_uri: str
    all_cols: str
    
    # API Config
    api_title: str
    api_description: str
    api_version: str
    
    ## Model 1 : Diagnosis
    mlflow_maladie: str
    bentoml_maladie: str
    
    ## Mapping : Diagnosis
    mapping_diagnosis: str
    
    ## Model 2 : Treatment
    mlflow_traitement: str
    bentoml_traitement: str
    
    ## Maaping : Treatment
    mapping_treatment: str
    
    # Default Config
    model_config = SettingsConfigDict(
        extra="allow",
        env_file= env_file
    )

# 3. Instantiate settings
try:
    settings = Settings()
except ValidationError as e:
    print("❌ Environment variable validation error :")
    print(e)
    settings = None
except FileNotFoundError as e:
    print(f"⚠️ Fichier .env missing : {e}")
    settings = None
    sys.exit(1)