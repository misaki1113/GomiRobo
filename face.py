import cv2

def get_face_position():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(50, 50))

        face_x, face_y = None, None
        if len(faces) > 0:
            x, y, w, h = faces[0]  # 最初の顔の座標を取得
            face_x = x + w // 2  # 顔の中心のX座標
            face_y = y + h // 2  # 顔の中心のY座標

        yield face_x, face_y, frame.shape[1], frame.shape[0]  # 顔のX/Y座標と画面幅/高さを返す

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
