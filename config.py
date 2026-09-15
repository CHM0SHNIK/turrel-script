"""Настройки проекта: путь к модели и список landmark'ов, по которым может наводиться турель."""

MODEL_PATH = "pose_landmarker_lite.task"

# Название -> индекс landmark'а (MediaPipe Pose, 33 точки)
LANDMARKS = {
    "nose": 0,           # нос / голова
    "left_wrist": 15,    # левое запястье
    "right_wrist": 16,   # правое запястье
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_hip": 23,
    "right_hip": 24,
}

DEFAULT_TARGET = "nose"

# Максимальные углы поворота турели (градусы)
MAX_PAN_ANGLE = 90
MAX_TILT_ANGLE = 60