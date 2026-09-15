"""Точка входа: захват видео, детекция позы, наведение, отображение."""

import cv2

from core.camera import Camera
from core.detection import PoseDetector
from core.targeting import Targeting
from core.display import Display
from core.peopleselector import PeopleSelector
from config import MODEL_PATH, MAX_PEOPLE

WINDOW_NAME = "Turret AI test"


def main():
    camera = Camera(0)
    detector = PoseDetector(MODEL_PATH, num_poses=MAX_PEOPLE)
    targeting = Targeting()
    display = Display()
    people = PeopleSelector()

    print("ESC — выход, N — переключить target, M — переключить вид отображения, P — переключить человека")

    while camera.is_opened():
        ret, frame = camera.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        poses = detector.detect(frame)
        poses = people.update(poses, ref_landmark_index=targeting.target_index)
        landmarks = people.selected(poses)

        result = targeting.compute(landmarks, w, h)

        if result:
            tx, ty, pan_angle, tilt_angle = result
            cx, cy = w // 2, h // 2

            other_points = [targeting.point_for(lm, w, h) for lm in poses]
            display.draw_people(frame, other_points, people.selected_idx)

            bbox = targeting.compute_bbox(landmarks, w, h)
            display.draw(frame, tx, ty, bbox, cx, cy)

            cv2.putText(
                frame,
                f"person={people.selected_idx + 1}/{len(poses)} target={targeting.target_name} "
                f"view={display.mode} pan={pan_angle:.1f} tilt={tilt_angle:.1f}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
            )

        cv2.imshow(WINDOW_NAME, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key in (ord("n"), ord("N")):
            targeting.next_target()
        elif key in (ord("m"), ord("M")):
            display.next_mode()
        elif key in (ord("p"), ord("P")):
            people.next_person()

    camera.release()
    cv2.destroyAllWindows()
    detector.close()


if __name__ == "__main__":
    main()