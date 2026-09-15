import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "pose_landmarker_lite.task"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1,
)
landmarker = vision.PoseLandmarker.create_from_options(options)

TARGET_LANDMARK = 0  # 0 = nose (голова); 15/16 = левое/правое запястье (рука)

cap = cv2.VideoCapture(0)
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
                         data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    timestamp_ms = int((time.time() - start_time) * 1000)
    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    if result.pose_landmarks:
        lm = result.pose_landmarks[0][TARGET_LANDMARK]
        tx, ty = int(lm.x * w), int(lm.y * h)
        cx, cy = w // 2, h // 2
        offset_x, offset_y = tx - cx, ty - cy

        pan_angle = offset_x / w * 90
        tilt_angle = offset_y / h * 60

        cv2.circle(frame, (tx, ty), 8, (0, 0, 255), -1)
        cv2.line(frame, (cx, cy), (tx, ty), (0, 255, 0), 2)
        cv2.putText(frame, f"pan={pan_angle:.1f} tilt={tilt_angle:.1f}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Turret AI test", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
landmarker.close()