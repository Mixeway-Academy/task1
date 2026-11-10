# Używamy oficjalnego obrazu Pythona
FROM python:3.9-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Instalujemy zależności (osobna warstwa - szybsze przebudowy)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy pliki projektu do kontenera
COPY . .
RUN chmod +x entrypoint.sh

# Ustawiamy zmienną środowiskową, aby Flask wiedział, jak uruchomić aplikację
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Najpierw testy jednostkowe, aplikacja startuje tylko gdy wszystkie przejdą
CMD ["./entrypoint.sh"]
