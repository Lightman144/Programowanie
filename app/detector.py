import cv2

class PersonDetector:
    def __init__(self) -> None: # Inicjalizacja klasycznego detektora HOG
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, image_path: str, output_path: str) -> int:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR) # Wczytanie obrazu
        if image is None:
            raise ValueError("Cannot read image")

        h, w = image.shape[:2]
        if w > 800:
            scale = 800 / w
            image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

        boxes, _ = self.hog.detectMultiScale( # Detekcja sylwetek ludzi
            image,
            winStride=(6, 6),
            padding=(8, 8),
            scale=1.08
        )

        filtered = []
        for (x, y, bw, bh) in boxes: # Rysowanie prostokątów
            if bh > 1.3 * bw:
                filtered.append((x, y, bw, bh))
                cv2.rectangle(image, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

        cv2.imwrite(output_path, image) # Zapis obrazu wynikowego
        return len(filtered)

