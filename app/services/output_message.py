# app/services/output_message.py
import sys
import json
import logging
from datetime import datetime
from app.config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== Upload MAPPING ======
# Diagnosis
with open(settings.mapping_diagnosis, encoding="utf-8") as f:
    diagnosis_mapping = json.load(f)

# Treatment
with open(settings.mapping_treatment, encoding="utf-8") as f:
    treatment_mapping = json.load(f)

# ====== FUNCTION OUTPUT MESSAGE ======
def format_output(diagnosis_pred: int,treatment_pred: int, model_type: str, latency_ms: float) -> dict:
    try:
        diagnosis = diagnosis_mapping.get(str(int(diagnosis_pred)), f"Unknown Disease ({diagnosis_pred})")
        treatment = treatment_mapping.get(str(int(treatment_pred)), f"Unknown Treatment ({treatment_pred})")

        # ---- Human-readable texte médical ----
        report_text = (
            f"L'examen clinique et les données analysées indiquent que vous souffrez de 🩺: {diagnosis}. "
            f"Sur la base de ce constat, et en tenant compte d'autres facteurs médicaux pertinents, "
            f"nous vous recommandons le traitement suivant 💊: {treatment}. "
            f"Veuillez consulter un médecin pour un suivi adapté et une confirmation clinique."
        )

        return {
            "⏲️ Timestamp": datetime.utcnow().isoformat(),
            "🔃 Model Used": model_type,
            "📊 Latency_ms": round(latency_ms, 2),
            "🤒 Diagnosis": diagnosis,
            "💊 Treatment": treatment,
            "👨‍⚕️ Examination Report": report_text
        }

    except Exception as e:
        logger.error(f"❌ Error Detected: {e}")
        logger.exception("🔃 Stack Trace :")
        sys.exit(1)