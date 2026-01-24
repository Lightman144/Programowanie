from flask import Flask
from app.api import register_routes
from app.worker import start_workers

# Tworzy i konfiguruje aplikację Flask
def create_app() -> Flask:
    app = Flask(__name__)
    register_routes(app) # rejestracja endpointów API
    return app

# Inicjalizacja aplikacji
app = create_app()
# Uruchomienie workerów asynchronicznych (wątków)
start_workers(count=8)

# Start serwera HTTP
if __name__ == "__main__":
    app.run(debug=True)
