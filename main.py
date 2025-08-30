# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config_api import settings
from app.routes.routes import router as prediction_router
from app.monitor import set_metrics

# === Création de l'application ===
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# === Middleware CORS (utile pour intégration avec front Django/React) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre si tu connais le domaine frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Monitoring Prometheus ===
set_metrics(app)

# === Enregistrement des routes ===
app.include_router(prediction_router)

# === Lancement direct ===
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
