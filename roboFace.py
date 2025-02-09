import pygame
import threading
import time
import random
from face import get_face_position

# 画面設定
WIDTH, HEIGHT = 800, 480
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 目の基本位置
eye_left_x = WIDTH // 3
eye_right_x = WIDTH * 2 // 3
eye_y = (HEIGHT // 2) - (HEIGHT // 4)

# 目のサイズ設定
EYE_RADIUS = 60  # 白目の半径
IRIS_RADIUS = 40  # 黒目の半径
MAX_IRIS_MOVEMENT = EYE_RADIUS - IRIS_RADIUS  # 黒目の可動範囲

# 黒目の初期位置
iris_left_x = eye_left_x
iris_right_x = eye_right_x
iris_left_y = eye_y
iris_right_y = eye_y

# 瞬きの状態
blink_level = 0  # 0: 開いてる, 10: 閉じてる
blinking = False

# くちばしの開閉レベル
beak_open_level = 0  

def draw_eyes(left_eye_pos, right_eye_pos, left_iris_pos, right_iris_pos, blink):
    screen.fill((233, 244, 252))  # 背景を白に

    # 左目（白目）
    pygame.draw.circle(screen, (113, 98, 70), left_eye_pos, EYE_RADIUS, 3)
    # 右目（白目）
    pygame.draw.circle(screen, (113, 98, 70), right_eye_pos, EYE_RADIUS, 3)

    # 左目（黒目）
    pygame.draw.circle(screen, (71, 75, 66), left_iris_pos, IRIS_RADIUS,38)
    # 右目（黒目）
    pygame.draw.circle(screen, (71, 75, 66), right_iris_pos, IRIS_RADIUS,38)

    # 瞬き（まぶた）
    if blink > 0:
        blink_height = int((blink / 10) * (EYE_RADIUS * 2))  # 瞬きの割合
        eyelid_color = (233, 244, 252)  # まぶたの色
        eyelash_color = (180, 190, 200)  # まつげ（下の辺）の色

        # 上からまぶたを覆う
        pygame.draw.rect(screen, eyelid_color, 
                         (left_eye_pos[0] - EYE_RADIUS, left_eye_pos[1] - EYE_RADIUS, EYE_RADIUS * 2, blink_height))
        pygame.draw.rect(screen, eyelid_color, 
                         (right_eye_pos[0] - EYE_RADIUS, right_eye_pos[1] - EYE_RADIUS, EYE_RADIUS * 2, blink_height))

        # 下の辺にまつげのラインを描く
        pygame.draw.line(screen, eyelash_color, 
                         (left_eye_pos[0] - EYE_RADIUS, left_eye_pos[1] - EYE_RADIUS + blink_height),
                         (left_eye_pos[0] + EYE_RADIUS, left_eye_pos[1] - EYE_RADIUS + blink_height), 3)
        pygame.draw.line(screen, eyelash_color, 
                         (right_eye_pos[0] - EYE_RADIUS, right_eye_pos[1] - EYE_RADIUS + blink_height),
                         (right_eye_pos[0] + EYE_RADIUS, right_eye_pos[1] - EYE_RADIUS + blink_height), 3)
    
def draw_penguin_mouth(center_x, center_y, open_level):
    """ ペンギンのくちばしを描画する（口を開くときに上と下の三角形を離す） """
    beak_color = (248, 184, 98)  # オレンジ色
    beak_outline = (253, 222, 165)  # 輪郭色

    # くちばしの移動量
    beak_movement = open_level * 2  # 口の開きに応じた移動量

    # 上のくちばし（上へ移動）
    top_beak = [
        (center_x - 110, center_y - beak_movement), 
        (center_x + 110, center_y - beak_movement), 
        (center_x, center_y - 40 - beak_movement)
    ]
    pygame.draw.polygon(screen, beak_color, top_beak)
    pygame.draw.polygon(screen, beak_outline, top_beak, 2)

    # 下のくちばし（下へ移動）
    bottom_beak = [
        (center_x - 110, center_y + beak_movement), 
        (center_x + 110, center_y + beak_movement), 
        (center_x, center_y + 40 + beak_movement)
    ]
    pygame.draw.polygon(screen, beak_color, bottom_beak)
    pygame.draw.polygon(screen, beak_outline, bottom_beak, 2)



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

# くちばしの開閉
def beak_animation():
    global beak_open_level
    while True:
        time.sleep(random.uniform(2, 5))  # 2〜5秒ごとに開閉
        for i in range(1, 5):  # 開く
            beak_open_level = i
            time.sleep(0.05)
        for i in range(4, -1, -1):  # 閉じる
            beak_open_level = i
            time.sleep(0.05)


def draw_bowtie(center_x, center_y):
    """ 蝶ネクタイを描画する """
    # #赤色
    # bowtie_color = (240, 144, 141)
    # outline_color = (240, 145, 153)

    # #青色
    # bowtie_color = (44, 169, 225)  
    # outline_color = (137, 195, 235)

    #黄色
    bowtie_color = (255, 236, 71)  
    outline_color = (245, 229, 107)

    # 左の三角形
    left_bowtie = [
        (center_x - 20, center_y),
        (center_x - 150, center_y - 50),
        (center_x - 150, center_y + 50)
    ]
    pygame.draw.polygon(screen, bowtie_color, left_bowtie)
    pygame.draw.polygon(screen, outline_color, left_bowtie, 2)

    # 右の三角形
    right_bowtie = [
        (center_x + 20, center_y),
        (center_x + 150, center_y - 50),
        (center_x + 150, center_y + 50)
    ]
    pygame.draw.polygon(screen, bowtie_color, right_bowtie)
    pygame.draw.polygon(screen, outline_color, right_bowtie, 2)

    # 真ん中の円（結び目）
    pygame.draw.circle(screen, outline_color, (center_x, center_y), 20)
    pygame.draw.circle(screen, bowtie_color, (center_x, center_y), 20)



# スレッド開始
threading.Thread(target=update_eye_position, daemon=True).start()
threading.Thread(target=blink_animation, daemon=True).start()
threading.Thread(target=beak_animation, daemon=True).start()

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

    draw_penguin_mouth(WIDTH // 2, HEIGHT // 2 + 5, beak_open_level)
    draw_bowtie(WIDTH // 2, HEIGHT // 2 + 140)  # 口の下に蝶ネクタイを描画

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
