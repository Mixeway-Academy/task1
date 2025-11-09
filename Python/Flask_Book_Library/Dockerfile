# Używamy oficjalnego obrazu Pythona
FROM python:3.9-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki projektu do kontenera
COPY . .

# Instalujemy zależności
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Gdy testy się nie zakończą się sukcesem obraz się nie zbuduj
RUN pytest -v

# Ustawiamy zmienną środowiskową, aby Flask wiedział, jak uruchomić aplikację
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Uruchamiamy aplikację
CMD ["flask", "run"]