# Étape 1 : Choisir une image de base
FROM python:3.9-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier ton fichier app.py dans le conteneur
COPY app.py .

# Étape 4 : Installer Flask et prometheus-flask-exporter
RUN pip install flask prometheus-flask-exporter twilio

# Étape 5 : Exposer le port 5000
EXPOSE 5000

# Étape 6 : Lancer l'application
CMD ["python", "app.py"]

