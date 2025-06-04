from fastapi import FastAPI
from src.api.config_api import settings
from src.api.routes import predict_disease
from src.api.prometheus import set_metrics

app = FastAPI(
    title=settings.api_title,
    description= settings.api_description,
    version=settings.api_version
)

app.include_router(predict_disease.router)

set_metrics(app)