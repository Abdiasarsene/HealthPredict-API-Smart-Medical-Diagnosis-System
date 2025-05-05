CREATE TABLE patients_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    pulse FLOAT,
    blood_pressure FLOAT,
    spo2 FLOAT,
    respiratory_rate FLOAT,
    bmi FLOAT,
    fasting_glucose FLOAT,
    cholesterol FLOAT,
    stress_level FLOAT,
    predicted_diagnosis VARCHAR(50),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
