# backend.Dockerfile

# Verwende ein offizielles Python-Image als Basis. Alpine ist schlank.
FROM python:3.12-alpine

# Metadaten für das Image
LABEL maintainer="mihai@developerakademie.com"
LABEL version="1.0"
LABEL description="Python 3.12 Alpine - Development Setup"

# Erstelle und setze das Arbeitsverzeichnis im Container
WORKDIR /app

# --- Umgebungs-Setup ---
# Installiere zuerst Systemabhängigkeiten. Dies bleibt für die Entwicklung wichtig,
# damit Pakete wie psycopg2 korrekt gebaut werden können.
RUN apk update && \
    apk add --no-cache --upgrade bash && \
    apk add --no-cache postgresql-client ffmpeg && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# --- Python-Abhängigkeiten ---
# Kopiere NUR die requirements.txt, um den Docker-Layer-Cache optimal zu nutzen.
# Solange sich diese Datei nicht ändert, wird der nächste Schritt nicht erneut ausgeführt.
COPY requirements.txt .

# Installiere die Python-Pakete
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Lösche die Build-Abhängigkeiten wieder, um das Image klein zu halten
RUN apk del .build-deps

# --- Für die Entwicklung auskommentiert ---
# Der Code wird nun über ein Volume in der docker-compose.yml gemountet,
# anstatt ihn direkt in das Image zu kopieren. Dies ermöglicht Live-Reloading.
# COPY . .

# Der chmod-Befehl ist nicht mehr nötig, da die Datei über das Volume
# gemountet wird und die Berechtigungen vom Host-System übernimmt.
# Führe `chmod +x backend.entrypoint.sh` einmal auf deinem Computer aus.
# chmod +x backend.entrypoint.sh

# Definiere den Standard-Port
EXPOSE 8000

# Der ENTRYPOINT wird für mehr Flexibilität in der Entwicklung
# direkt in der docker-compose.yml als 'command' überschrieben.
# ENTRYPOINT [ "./backend.entrypoint.sh" ]
