import mysql.connector
import logging

def insert_patient_data(data, diagnosis):
    try:
        connection = mysql.connector.connect(
            host="localhost",  # ou ton host Docker
            user="root",
            password="",
            database="health_predict"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO patients_data 
        (temperature, pulse, blood_pressure, spo2, respiratory_rate, bmi, fasting_glucose, cholesterol, stress_level, predicted_diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data.Temperature, 
            data.Pulse, 
            data.BloodPressure, 
            data.SpO2, 
            data.RespiratoryRate,
            data.BMI, 
            data.FastingGlucose, 
            data.Cholesterol, 
            data.StressLevel,
            diagnosis
        )

        cursor.execute(insert_query, values)
        connection.commit()
        cursor.close()
        connection.close()

        print("✅ Données insérées avec succès dans la base de données.")
    except mysql.connector.Error as err:
        logging.error(f"❌ Erreur MySQL: {err}")
        print(f"❌ Erreur lors de l'insertion dans la base de données : {err}")
    except Exception as e:
        logging.error(f"❌ Erreur générale: {e}")
        print(f"❌ Erreur lors de l'insertion dans la base de données : {e}")
