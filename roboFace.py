import pygame
import threading
from face import get_face_position

# 画面設定
WIDTH, HEIGHT = 400, 200
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 目の基本位置
eye_left_x = WIDTH // 3
eye_right_x = WIDTH * 2 // 3
eye_y = HEIGHT // 2

# 目のサイズ設定
EYE_RADIUS = 30  # 白目の半径
IRIS_RADIUS = 10  # 黒目の半径
MAX_IRIS_MOVEMENT = EYE_RADIUS - IRIS_RADIUS  # 黒目が動ける最大距離（左右 & 上下）

# 黒目の初期位置
iris_left_x = eye_left_x
iris_right_x = eye_right_x
iris_left_y = eye_y
iris_right_y = eye_y

def draw_eyes(left_eye_pos, right_eye_pos, left_iris_pos, right_iris_pos):
    screen.fill((255, 255, 255))  # 背景を白に

    # 左目（白目）
    pygame.draw.circle(screen, (0, 0, 0), left_eye_pos, EYE_RADIUS, 3)
    # 左目（黒目）
    pygame.draw.circle(screen, (0, 0, 0), left_iris_pos, IRIS_RADIUS)

    # 右目（白目）
    pygame.draw.circle(screen, (0, 0, 0), right_eye_pos, EYE_RADIUS, 3)
    # 右目（黒目）
    pygame.draw.circle(screen, (0, 0, 0), right_iris_pos, IRIS_RADIUS)

# カメラ処理をスレッドで実行
def update_eye_position():
    global iris_left_x, iris_right_x, iris_left_y, iris_right_y

    for face_x, face_y, frame_width, frame_height in get_face_position():
        if face_x is not None and face_y is not None:
            # 顔のX位置を目の範囲内にスケール変換（左右）
            normalized_x = 1 - (face_x / frame_width) * 2  # -1 (左端) 〜 1 (右端)
            iris_left_x = eye_left_x + int(normalized_x * MAX_IRIS_MOVEMENT)
            iris_right_x = eye_right_x + int(normalized_x * MAX_IRIS_MOVEMENT)

            # 顔のY位置を目の範囲内にスケール変換（上下）
            normalized_y = (face_y / frame_height) * 2 - 1  # -1 (上端) 〜 1 (下端)
            iris_left_y = eye_y + int(normalized_y * MAX_IRIS_MOVEMENT)
            iris_right_y = eye_y + int(normalized_y * MAX_IRIS_MOVEMENT)

            # 黒目の移動範囲を制限（白目からはみ出さない）
            iris_left_x = max(eye_left_x - MAX_IRIS_MOVEMENT, min(iris_left_x, eye_left_x + MAX_IRIS_MOVEMENT))
            iris_right_x = max(eye_right_x - MAX_IRIS_MOVEMENT, min(iris_right_x, eye_right_x + MAX_IRIS_MOVEMENT))
            iris_left_y = max(eye_y - MAX_IRIS_MOVEMENT, min(iris_left_y, eye_y + MAX_IRIS_MOVEMENT))
            iris_right_y = max(eye_y - MAX_IRIS_MOVEMENT, min(iris_right_y, eye_y + MAX_IRIS_MOVEMENT))

# スレッド開始
threading.Thread(target=update_eye_position, daemon=True).start()

# pygame メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_eyes(
        (eye_left_x, eye_y), 
        (eye_right_x, eye_y), 
        (iris_left_x, iris_left_y), 
        (iris_right_x, iris_right_y)
    )

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
