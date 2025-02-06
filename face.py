import cv2

def detect_faces():
    # カスケード分類器のファイルパス
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # カメラキャプチャを開始
    cap = cv2.VideoCapture(0)

    while True:
        # フレームをキャプチャ
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # グレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔を検出
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(50, 50))

        print(faces)

        
        # 検出した顔に四角を描画
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # フレームを表示
        cv2.imshow('Face Detection', frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # リリースとウィンドウの破棄
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_faces()
