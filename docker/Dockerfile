# Étape 1 : Utiliser une image officielle Python
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY requirements.txt .

# Étape 4 : Installer les dépendances systèmes minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Étape 5 : Installer les dépendances Python
RUN pip install --upgrade pip \
    && pip install -default-timeout=100 --no-cache-dir -r requirements.txt

# Etape 6 : Copier le reste du code après l'installation
COPY . . 

# Etape 7 : Exposer le port de l'API 
EXPOSE 8000

# Étape 6 : Commande pour lancer le serveur
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
