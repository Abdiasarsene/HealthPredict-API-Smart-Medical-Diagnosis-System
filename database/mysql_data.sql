-- Active: 1746491695893@@localhost@3306@health_predict
CREATE TABLE patients_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Temperature FLOAT,
    Pulse FLOAT,
    BloodPressure FLOAT,
    SpO2 FLOAT,
    RespiratoryRate FLOAT,
    BMI FLOAT,
    FastingGlucose FLOAT,
    Cholesterol FLOAT,
    StressLevel FLOAT,
    Fatigue_intense ENUM("Présent","Absent") NOT NULL,
    Frissons ENUM("Présent","Absent") NOT NULL,
    Perte_gout_odorat ENUM("Présent","Absent") NOT NULL,
    Toux_seche ENUM("Présent","Absent") NOT NULL,
    predicted_diagnosis VARCHAR(50),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM patients_data ORDER BY prediction_date DESC ;

INSERT INTO patients_data (Temperature, Pulse, BloodPressure, SpO2, RespiratoryRate, BMI, FastingGlucose, Cholesterol, StressLevel, Fatigue_intense, Frissons, Perte_gout_odorat, Toux_seche, predicted_diagnosis)
VALUES (37.5, 80, 120, 98, 16, 22.0, 90, 180, 5, 'Présent', 'Absent', 'Absent', 'Absent', 'Grippe');