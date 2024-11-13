# Używamy oficjalnego obrazu Pythona
FROM python:3.9-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki projektu do kontenera
COPY . .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Ustawiamy zmienną środowiskową, aby Flask wiedział, jak uruchomić aplikację
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Argument do uruchamiania aplikacji/testów
ARG RUN_TESTS=False

# Uruchamiamy aplikację/testy
CMD if [ "$RUN_TESTS" = "True" ]; then python -m unittest discover -s tests -p "test_xss.py"; else flask run; fi
