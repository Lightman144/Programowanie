import uuid
import os
import requests
from flask import request, jsonify
from app.task_queue import task_queue
from app.storage import storage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Katalog bazowy projektu
IMAGE_DIR = os.path.join(BASE_DIR, "images", "input") # Katalog wejściowy na obrazy

# Dodanie zadania do kolejki
def enqueue_task(task_id: str, image_path: str) -> None:
    storage.create_task(task_id)
    task_queue.put({
        "task_id": task_id,
        "image_path": image_path
    })

def register_routes(app):
    @app.route("/detect/local", methods=["GET"])
    def detect_local():
        filename = request.args.get("filename")
        path = os.path.join(IMAGE_DIR, filename)

        # Sprawdzenie czy plik istnieje
        if not os.path.exists(path):
            return jsonify({"error": "file not found"}), 404

        task_id = str(uuid.uuid4()) # Generowanie ID zadania
        storage.create_task(task_id) # Rejestracja zadania w storage
        enqueue_task(task_id, path) # Dodanie zadania do kolejki

        return jsonify({"task_id": task_id}) # Zwrócenie ID zadania

    @app.route("/detect/url", methods=["GET"])
    def detect_url():
        image_url = request.args.get("image_url")   # URL obrazu
        task_id = str(uuid.uuid4())

        response = requests.get(image_url)  # Pobranie obrazu z internetu
        path = os.path.join(IMAGE_DIR, f"{task_id}.jpg") # Ścieżka zapisu obrazu

        with open(path, "wb") as f: # Zapis obrazu na dysku
            f.write(response.content)

        storage.create_task(task_id) # Rejestracja zadania
        enqueue_task(task_id, path)

        return jsonify({"task_id": task_id})

    @app.route("/detect/raw", methods=["POST"])
    def detect_raw():
        raw = request.data
        if not raw:
            return jsonify({"error": "empty body"}), 400

        task_id = str(uuid.uuid4())
        input_path = os.path.join(IMAGE_DIR, f"{task_id}.jpg") # Ścieżka zapisu obrazu

        with open(input_path, "wb") as f:   # Zapis obrazu
            f.write(raw)

        if not os.path.exists(input_path):
            return jsonify({"error": "file not saved"}), 500

        storage.create_task(task_id)
        enqueue_task(task_id, input_path)

        return jsonify({"task_id": task_id})

    @app.route("/tasks/<task_id>", methods=["GET"])
    def task_status(task_id: str):
        task = storage.get(task_id) # Pobranie statusu zadania
        if not task:
            return jsonify({"error": "not found"}), 404
        return jsonify(task)