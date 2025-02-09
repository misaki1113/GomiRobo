import pygame
import threading
import time
import random
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
MAX_IRIS_MOVEMENT = EYE_RADIUS - IRIS_RADIUS  # 黒目の可動範囲

# 黒目の初期位置
iris_left_x = eye_left_x
iris_right_x = eye_right_x
iris_left_y = eye_y
iris_right_y = eye_y

# 瞬きの状態
blink_level = 0  # 0: 開いてる, 10: 閉じてる
blinking = False

def draw_eyes(left_eye_pos, right_eye_pos, left_iris_pos, right_iris_pos, blink):
    screen.fill((255, 255, 255))  # 背景を白に

    # 左目（白目）
    pygame.draw.circle(screen, (0, 0, 0), left_eye_pos, EYE_RADIUS, 3)
    # 右目（白目）
    pygame.draw.circle(screen, (0, 0, 0), right_eye_pos, EYE_RADIUS, 3)

    # 左目（黒目）
    pygame.draw.circle(screen, (0, 0, 0), left_iris_pos, IRIS_RADIUS)
    # 右目（黒目）
    pygame.draw.circle(screen, (0, 0, 0), right_iris_pos, IRIS_RADIUS)

    # 瞬き（上から矩形で隠す）
    if blink > 0:
        blink_height = int((blink / 10) * (EYE_RADIUS * 2))  # 閉じる割合
        pygame.draw.rect(screen, (255, 255, 255), (left_eye_pos[0] - EYE_RADIUS, left_eye_pos[1] - EYE_RADIUS, EYE_RADIUS * 2, blink_height))
        pygame.draw.rect(screen, (255, 255, 255), (right_eye_pos[0] - EYE_RADIUS, right_eye_pos[1] - EYE_RADIUS, EYE_RADIUS * 2, blink_height))

# カメラ処理をスレッドで実行
def update_eye_position():
    global iris_left_x, iris_right_x, iris_left_y, iris_right_y

    for face_x, face_y, frame_width, frame_height in get_face_position():
        if face_x is not None and face_y is not None:
            normalized_x = 1 - (face_x / frame_width) * 2  # 左右の動き
            iris_left_x = eye_left_x + int(normalized_x * MAX_IRIS_MOVEMENT)
            iris_right_x = eye_right_x + int(normalized_x * MAX_IRIS_MOVEMENT)

            normalized_y = (face_y / frame_height) * 2 - 1  # 上下の動き
            iris_left_y = eye_y + int(normalized_y * MAX_IRIS_MOVEMENT)
            iris_right_y = eye_y + int(normalized_y * MAX_IRIS_MOVEMENT)

            # 移動範囲の制限
            iris_left_x = max(eye_left_x - MAX_IRIS_MOVEMENT, min(iris_left_x, eye_left_x + MAX_IRIS_MOVEMENT))
            iris_right_x = max(eye_right_x - MAX_IRIS_MOVEMENT, min(iris_right_x, eye_right_x + MAX_IRIS_MOVEMENT))
            iris_left_y = max(eye_y - MAX_IRIS_MOVEMENT, min(iris_left_y, eye_y + MAX_IRIS_MOVEMENT))
            iris_right_y = max(eye_y - MAX_IRIS_MOVEMENT, min(iris_right_y, eye_y + MAX_IRIS_MOVEMENT))

# 瞬き処理をスレッドで実行
def blink_animation():
    global blink_level, blinking
    while True:
        time.sleep(random.uniform(3, 6))  # 3秒〜6秒ごとに瞬き
        blinking = True
        for i in range(1, 11):  # ゆっくり閉じる
            blink_level = i
            time.sleep(0.05)
        time.sleep(0.1)  # 閉じた状態を維持
        for i in range(9, -1, -1):  # ゆっくり開く
            blink_level = i
            time.sleep(0.05)
        blinking = False

# スレッド開始
threading.Thread(target=update_eye_position, daemon=True).start()
threading.Thread(target=blink_animation, daemon=True).start()

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
        (iris_right_x, iris_right_y), 
        blink_level
    )

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
