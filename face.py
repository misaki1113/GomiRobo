import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
face_detector = mp_face_detection.FaceDetection(min_detection_confidence=0.6)

def get_face_position():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detector.process(rgb_frame)

        face_x, face_y = None, None
        if results.detections:
            detection = results.detections[0]  # 最初の顔のみ取得
            bbox = detection.location_data.relative_bounding_box

            face_x = int((bbox.xmin + bbox.width / 2) * frame.shape[1])
            face_y = int((bbox.ymin + bbox.height / 2) * frame.shape[0])

        yield face_x, face_y, frame.shape[1], frame.shape[0]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
