from config import LANDMARKS, DEFAULT_TARGET, MAX_PAN_ANGLE, MAX_TILT_ANGLE


class Targeting:
    def __init__(self, target_name=DEFAULT_TARGET):
        self._names = list(LANDMARKS.keys())
        self.set_target(target_name)

    def set_target(self, target_name):
        if target_name not in LANDMARKS:
            raise ValueError(f"Неизвестный target: {target_name}. Доступны: {self._names}")
        self.target_name = target_name
        self.target_index = LANDMARKS[target_name]

    def next_target(self):
        """Переключиться на следующий landmark в списке (например по нажатию клавиши)."""
        i = self._names.index(self.target_name)
        self.set_target(self._names[(i + 1) % len(self._names)])

    def compute(self, landmarks, frame_w, frame_h):
        """Возвращает (tx, ty, pan_angle, tilt_angle) для текущего target'а, либо None."""
        if landmarks is None or self.target_index >= len(landmarks):
            return None

        lm = landmarks[self.target_index]
        tx, ty = int(lm.x * frame_w), int(lm.y * frame_h)
        cx, cy = frame_w // 2, frame_h // 2
        offset_x, offset_y = tx - cx, ty - cy

        pan_angle = offset_x / frame_w * MAX_PAN_ANGLE
        tilt_angle = offset_y / frame_h * MAX_TILT_ANGLE

        return tx, ty, pan_angle, tilt_angle

    def compute_bbox(self, landmarks, frame_w, frame_h, padding=0.05):
        if not landmarks:
            return None

        xs = [lm.x for lm in landmarks]
        ys = [lm.y for lm in landmarks]
        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)

        pad_x = (x2 - x1) * padding
        pad_y = (y2 - y1) * padding

        x1 = int(max(0, (x1 - pad_x) * frame_w))
        x2 = int(min(frame_w, (x2 + pad_x) * frame_w))
        y1 = int(max(0, (y1 - pad_y) * frame_h))
        y2 = int(min(frame_h, (y2 + pad_y) * frame_h))

        return x1, y1, x2, y2
    def point_for(self, landmarks, frame_w, frame_h):
        """Координаты текущего target landmark'а для произвольного набора
        landmark'ов — используется, чтобы отметить на кадре всех людей."""
        if landmarks is None or self.target_index >= len(landmarks):
            return None
        lm = landmarks[self.target_index]
        return int(lm.x * frame_w), int(lm.y * frame_h)