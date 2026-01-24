from app.task_queue import task_queue, executor
from app.detector import PersonDetector
from app.storage import storage
import os
detector = PersonDetector()

def worker() -> None: # Worker przetwarzający zadania z kolejki
    while True:
        task = task_queue.get() # Pobranie zadania z kolejki
        if task is None:
            break

        task_id = task["task_id"]
        image_path = task["image_path"]

        storage.set_in_progress(task_id)

        try: # Ścieżka zapisu obrazu wynikowego
            base_name = os.path.basename(image_path)
            output_path = os.path.join(
                os.path.dirname(os.path.dirname(image_path)),
                "output",
                base_name
            )
            output_path = str(output_path)
            count = detector.detect(image_path, output_path) # Detekcja osób
            storage.set_done(task_id, count) # Zapis wyniku

        except Exception as e:
            storage.set_failed(task_id, str(e)) # Obsługa błędu

        finally:
            task_queue.task_done()

def start_workers(count: int = 4) -> None: # Uruchomienie wielu workerów
    for _ in range(count):
        executor.submit(worker)