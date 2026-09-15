import cv2


class Camera:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Не удалось открыть камеру {index}")

    def read(self):
        ret, frame = self.cap.read()
        return ret, frame

    def is_opened(self):
        return self.cap.isOpened()

    def release(self):
        self.cap.release()