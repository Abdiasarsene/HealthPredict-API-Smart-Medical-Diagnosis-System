# **HealthPredict — Smart Medical Diagnosis API**

![Ray Serve](https://img.shields.io/badge/Ray_Serve-00AEEF?style=for-the-badge&logo=ray&logoColor=white) 
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) 
![MLflow](https://img.shields.io/badge/MLflow-FF4F00?style=for-the-badge&logo=mlflow&logoColor=white) 
![BentoML](https://img.shields.io/badge/BentoML-FF6F61?style=for-the-badge&logo=bentoml&logoColor=white) 
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white) 
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white) 
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white) 
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) 
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white) 
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)

*"Healthcare decisions are life-critical. HealthPredict predicts medical outcomes, diagnoses risks, and guides treatment decisions with intelligent, traceable AI. Built for hospitals, clinics, and telemedicine platforms that demand reliability and speed."*

---

## 🎯 Goal : Designed for critical medical diagnosis workflows

* Predictive diagnosis for common and rare conditions
* Risk estimation based on structured medical data
* Dual-model architecture: Ray Serve for scalability + FastAPI fallback for robustness
* Modular pipelines for retraining and model versioning

---

## 🧠 Stack Used

* **Ray Serve**: distributed model serving → horizontal scalability for real-time predictions
* **FastAPI**: async-ready API layer → minimal latency, high throughput, fallback support
* **MLflow**: model lifecycle management → reproducibility, traceability, experiment tracking
* **BentoML**: fallback deployment → resilience under model or service failure
* **Prometheus + Grafana**: telemetry and alerting → operational visibility and drift detection
* **Jenkins CI/CD**: automated build and deploy → reproducible integration and delivery

💡 Each tool was chosen for **robustness, reliability, and maintainability**, not just aesthetics.

---

## ⚙️ Architecture

![HealthPredict Architecture](./statics/api.png)

---

## 📖 Backend Narrative

*"Patient data is ingested, validated, and preprocessed using robust encoding and normalization pipelines. Dual predictive models (diagnosis & treatment) are trained, versioned, and tracked via MLflow. Ray Serve delivers predictions in real-time while FastAPI ensures a fallback route for service continuity. Prometheus/Grafana monitor API latency, model drift, and request health, with CI/CD orchestrated by Jenkins. Retraining and evaluation pipelines are modular and ready for Airflow integration."*

---

## 💻 API Demonstration

![API Predictive](./statics/postman.png)

<div style="display: flex; gap: 20px;">

<div style="flex: 1;">
**Input Example**
<pre>
{
  "Fievre": "Présent",
  "Temperature": 30.2,
  "Pulse": 32.0,
  "BloodPressure": 120.0,
  "SpO2": 96.5,
  "RespiratoryRate": 16.0,
  "BMI": 24.5,
  "FastingGlucose": 78.0,
  "Cholesterol": 200.0,
  "StressLevel": 5.0
}
</pre>
</div>

<div style="flex: 1;">
**Output Example**
<pre>
{
    "⏲️ Timestamp": "2025-09-21T22:27:25.599414",
    "🔃 Model Used": "Unknown",
    "📊 Latency_ms": 57.01,
    "🤒 Diagnosis": "Asthme",
    "💊 Treatment": "Médicament",
    "👨‍⚕️ Examination Report": "L'examen clinique et les données analysées indiquent que vous souffrez de 🩺: Asthme. Sur la base de ce constat, et en tenant compte d'autres facteurs médicaux pertinents, nous vous recommandons le traitement suivant 💊: Médicament. Veuillez consulter un médecin pour un suivi adapté et une confirmation clinique."
}
</pre>
</div>

</div>

---

## 📊 Monitoring

*"Real-time monitoring: API latency, uptime, prediction counts, error rates, and model performance metrics for early detection of drift or anomalies in patient data streams."*

[![Dashboard Preview](./statics/grafana_preview.png)](https://drive.google.com/file/d/1uD0oQKDrmADOqS0NHQR6PEfOGW2Jhqwu/view?usp=drive_link)

---

## 📊 Operational Impact

* **>95% accuracy** in diagnosis predictions
* **<120ms latency** per prediction under production load
* **Auto-fallback** ensures uninterrupted service
* **Live monitoring** of model drift, API health, and data quality

---

## 🚀 Roadmap

* **Integration** of **real-time patient vitals** for dynamic risk scoring
* **Multi-model ensemble** for rare and complex diagnoses
* **Federated learning** across hospitals for privacy-preserving insights
* **Explainable AI** dashboards for clinicians and regulatory compliance
* **Telemedicine integration** for remote diagnostic support

---

## 🏁 Final Note

*"HealthPredict demonstrates how medical AI can be production-ready, modular, and reliable. The models are here, the architecture is solid — how far you take patient care is up to you."*

---

👤 **Abdias Arsène**
*Sr. AI Consultant — Architect of scalable intelligence* 🧠
