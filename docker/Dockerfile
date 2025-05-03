# Étape 1 : Utiliser une image officielle Python
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY . /app

# Étape 4 : Installer les dépendances
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn[standard] mlflow scikit-learn pandas

# Étape 5 : Exposer le port de l’API
EXPOSE 8000

# Étape 6 : Commande pour lancer le serveur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
