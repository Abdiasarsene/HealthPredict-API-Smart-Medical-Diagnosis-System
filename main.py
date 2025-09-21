# app/main.py
import logging
from fastapi import FastAPI

from app.routers.route import router as api_router
from app.monitor import add_monitoring, metrics_middleware
from app.secure import apply_security_middleware
from app.config import settings
from app.events.events_pipeline import register_startup_events

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO,)
logger = logging.getLogger("medical_orchestrator")


# ====== FASTAPI APP ======
def create_app() -> FastAPI:
    app = FastAPI(
        title= settings.api_title,
        description=settings.api_description,
        version=settings.api_version
    )

    # ===== Security Middleware (CORS, TrustedHost) =====
    apply_security_middleware(app)
    
    #  ===== Monitoring (Prometheus + Middleware) ======
    add_monitoring(app)
    app.middleware("http")(metrics_middleware)
    
    # ===== Startup : Chargement des Modèles
    register_startup_events(app)

    # ===== Include API routes =====
    app.include_router(api_router)
    
    logger.info("✅ FastAPI APP Created and Configured")
    return app


# ===== INSTANCE =====
app = create_app()