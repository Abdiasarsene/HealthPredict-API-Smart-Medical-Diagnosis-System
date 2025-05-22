-- Active: 1742555678699@@127.0.0.1@3306

-- ====== CREATION DE LA TABLE patients_data ======
CREATE TABLE IF NOT EXISTS patients_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Temperature FLOAT,
    Pulse FLOAT,
    BloodPressure FLOAT,
    SpO2 FLOAT,
    RespiratoryRate FLOAT,
    BMI FLOAT,
    FastingGlucose FLOAT,
    Cholesterol FLOAT,
    StressLevel FLOAT,
    Fatigue_intense TEXT NOT NULL,
    Frissons TEXT NOT NULL,
    Perte_gout_odorat TEXT NOT NULL,
    Toux_seche TEXT NOT NULL,
    predicted_diagnosis VARCHAR(50),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ====== INSERTION DES DONNEES MANUELLES ======
INSERT INTO patients_data (Temperature, Pulse, BloodPressure, SpO2, RespiratoryRate, BMI, FastingGlucose, Cholesterol, StressLevel, Fatigue_intense, Frissons, Perte_gout_odorat, Toux_seche, predicted_diagnosis)
VALUES (37.5, 80, 120, 98, 16, 22.0, 90, 180, 5, 'Présent', 'Absent', 'Absent', 'Absent', 'Grippe');

-- ====== VERIFICATION DES DONNEES ======
SELECT * FROM patients_data ORDER BY prediction_date DESC ;

-- ====== NOMBRE DE TABLES PRESENTES ======
SELECT name FROM sqlite_master WHERE type='table';