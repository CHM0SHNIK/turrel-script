"""Обёртка над MediaPipe PoseLandmarker (Tasks API)."""

import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class PoseDetector:
    def __init__(self, model_path, num_poses=1):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=num_poses,
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self._start_time = time.time()

    def detect(self, frame):
        """frame — кадр BGR из OpenCV. Возвращает список landmark'ов первого человека или None."""
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
        )
        timestamp_ms = int((time.time() - self._start_time) * 1000)
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.pose_landmarks:
            return result.pose_landmarks[0]
        return None

    def close(self):
        self.landmarker.close()