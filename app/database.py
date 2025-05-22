import os 
import sqlite3
import logging
from dotenv import load_dotenv

# ====== INIIALISATION DE LA BASE DE DONNEES ======

def init_db():
    try:
        database_sql = os.getenv("DATABASE_SQL")
        connection = sqlite3.connect(database_sql)  
        cursor = connection.cursor()

        # Charger et exécuter le script SQL
        with open("patients_data.sql", "r") as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        connection.commit()
        cursor.close()
        connection.close()

        logging.info("✅ Base de données et table patients_data créées !")
    
    except sqlite3.Error as err:
        logging.error(f"❌ Erreur SQLite lors de l'initialisation : {err}")

# ====== TEST D'INSERTION DIRECTE ======
def test_manual_insert():
    connection = sqlite3.connect("patients_data.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO patients_data 
    (Temperature, Pulse, BloodPressure, SpO2, 
    RespiratoryRate, BMI, 
    FastingGlucose, Cholesterol, StressLevel, 
    Fatigue_intense, Frissons, 
    Perte_gout_odorat, Toux_seche, predicted_diagnosis)
    VALUES (37.5, 80, 120, 98, 16, 22.0, 90, 180, 5, 'Présent', 'Absent', 'Absent', 'Absent', 'Grippe')
    """)

    connection.commit()
    cursor.close()
    connection.close()
    logging.info("✅ Test d’insertion réussi !")

# ====== INSERTION DES DONNEES DANS LA TABLE GRACE A L'API ======

def insert_patient_data(data, diagnosis):
    try:
        connection = sqlite3.connect("patients_data.db")
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO patients_data 
        (Temperature, 
        Pulse, BloodPressure, 
        SpO2, RespiratoryRate, 
        BMI, 
        FastingGlucose, 
        Cholesterol, 
        StressLevel, 
        Fatigue_intense, 
        Frissons, 
        Perte_gout_odorat, 
        Toux_seche, 
        predicted_diagnosis)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            data.Fatigue_intense, 
            data.Frissons,
            data.Perte_gout_odorat, 
            data.Toux_seche, 
            diagnosis
        )
        
        logging.info(f"📊 Données envoyées à SQLite : {values}")
        cursor.execute(insert_query, values)
        rows_affected = cursor.rowcount
        logging.info(f"🧐 Nombre de lignes affectées : {rows_affected}")
        connection.commit()
        cursor.close()
        connection.close()

        logging.info("✅ Données insérées avec succès dans SQLite !")

    except sqlite3.Error as err:
        logging.error(f"❌ Erreur SQLite : {err}")