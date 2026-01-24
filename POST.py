import requests
from pathlib import Path

API_URL = "http://127.0.0.1:5000/detect/raw"

current_dir = Path.cwd()

# Znalezienie wszystkich plików jpg w katalogu
images = list(current_dir.glob("*.jpg"))

if not images:
    print("Brak plików .jpg w katalogu")
    exit(0)

print(f"Znaleziono {len(images)} plików .jpg")

for image_path in images:
    print(f"Wysyłam: {image_path.name}")

    with image_path.open("rb") as f:
        data = f.read()

    try: # Wysłanie obrazu do API
        res = requests.post(
            API_URL,
            headers={"Content-Type": "application/octet-stream"},
            data=data,
            timeout=10
        )

        if res.ok:
            print("task_id:", res.json().get("task_id"))
        else:
            print("Błąd:", res.status_code, res.text)

    except Exception as e:
        print("Wyjątek:", e)