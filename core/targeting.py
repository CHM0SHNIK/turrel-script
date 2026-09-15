"""Логика наведения: выбор landmark'а и расчёт углов поворота турели."""

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