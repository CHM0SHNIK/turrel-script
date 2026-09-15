import cv2

from config import DISPLAY_MODES, DEFAULT_DISPLAY_MODE


class Display:
    def __init__(self, mode=DEFAULT_DISPLAY_MODE):
        self._modes = list(DISPLAY_MODES)
        self.set_mode(mode)

    def set_mode(self, mode):
        if mode not in self._modes:
            raise ValueError(f"Неизвестный режим отображения: {mode}. Доступны: {self._modes}")
        self.mode = mode

    def next_mode(self):
        i = self._modes.index(self.mode)
        self.set_mode(self._modes[(i + 1) % len(self._modes)])

    def draw(self, frame, tx, ty, bbox, cx, cy):
        if self.mode in ("point", "both"):
            cv2.circle(frame, (tx, ty), 8, (0, 0, 255), -1)

        if self.mode in ("bbox", "both") and bbox:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        cv2.line(frame, (cx, cy), (tx, ty), (0, 255, 0), 2)
    
    def draw_people(self, frame, points, selected_idx):
        for i, pt in enumerate(points):
            if pt is None or i == selected_idx:
                continue
            cv2.circle(frame, pt, 6, (180, 180, 180), -1)
            cv2.putText(frame, str(i + 1), (pt[0] + 8, pt[1] - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)