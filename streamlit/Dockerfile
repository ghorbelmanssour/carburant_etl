# streamlit/Dockerfile

FROM python:3.10-slim

# Installer les dépendances système (pour psycopg2)
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requis
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
