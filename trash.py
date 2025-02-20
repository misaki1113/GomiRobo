import RPi.GPIO as GPIO
import time

# ピン設定
TRIG_PIN = 9
ECHO_PIN = 10
LED_PIN = 13
SWITCH_PIN = 7
SERVO_PIN = 6
SPEAKER_PIN = 8

# 変数
detection_count = 0
threshold_distance = 30
is_servo = False

# GPIOの設定
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(SPEAKER_PIN, GPIO.OUT)

# サーボモーターの設定
def setup_servo():
    global servo
    servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
    servo.start(0)

# サーボを指定した角度に動かす関数
def move_servo(angle):
    pulse_width = angle / 18 + 2  # 0-180度をパルス幅にマッピング
    GPIO.output(SERVO_PIN, True)
    time.sleep(pulse_width / 1000)  # パルス幅をミリ秒単位で指定
    GPIO.output(SERVO_PIN, False)
    time.sleep(0.020 - pulse_width / 1000)  # 残りの周期をLOW状態に

# 超音波センサーから距離を取得する関数
def get_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.000002)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # パルスが戻ってくるまでの時間を測定
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance = duration * 17150  # 距離を計算（音速 343m/s）
    return distance

# スイッチの状態を確認し、必要な処理を行う関数
def check_switch():
    global detection_count, is_servo
    switch_state = GPIO.input(SWITCH_PIN)
    
    if switch_state == GPIO.LOW:
        detection_count = 0
        GPIO.output(LED_PIN, GPIO.LOW)
        is_servo = False
        move_servo(0)  # サーボを初期位置に戻す
        print("Counter reset")
        time.sleep(0.5)  # スイッチの押し間違いを防ぐためのディレイ

# 音を鳴らす関数
def sound_buzzer():
    GPIO.output(SPEAKER_PIN, True)
    time.sleep(0.2)  # 200ms音を鳴らす
    GPIO.output(SPEAKER_PIN, False)

# メインループ
def main():
    global detection_count, is_servo

    setup_gpio()
    setup_servo()

    try:
        while True:
            check_switch()
            distance = get_distance()
            print("Distance: {:.2f} cm".format(distance))

            if distance < threshold_distance:
                detection_count += 1
                print("Detection count:", detection_count)
                sound_buzzer()  # 音を鳴らす

                if detection_count >= 10 and not is_servo:
                    GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
                    print("LED is ON")
                    move_servo(90)  # サーボを90°に回転
                    is_servo = True
                    print("Servo is ON")

                time.sleep(0.5)  # 検知が10回未満の場合は待機

            time.sleep(1)  # 1秒ごとに距離を測定

    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        GPIO.cleanup()  # GPIOのクリーンアップ

if __name__ == "__main__":
    main()
