import sounddevice as sd
import numpy as np
import speech_recognition as sr
import wavio
import pygame

# 設定
SAMPLE_RATE = 16000  # サンプリングレート（16kHz）
DURATION = 5  # 録音時間（秒）
MP3_FILE = "hello.mp3"  # 再生するMP3ファイル

def play_audio(file_path):
    """MP3ファイルをpygameで再生"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # 再生が終わるまで待機
    except Exception as e:
        print(f"音声の再生中にエラーが発生しました: {e}")

def record_audio():
    """マイクから音声を録音してnumpy配列として返す"""
    print("話してください... ('おはよう' で音声再生 / '終了' でプログラム終了)")
    audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()  # 録音が終わるまで待機
    return audio_data

def save_wav(filename, audio_data):
    """録音した音声をWAVファイルとして保存"""
    wavio.write(filename, audio_data, SAMPLE_RATE, sampwidth=2)

def recognize_speech(audio_data):
    """録音した音声をテキストに変換"""
    recognizer = sr.Recognizer()
    save_wav("temp.wav", audio_data)
    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        print("認識結果:", text)
        return text
    except sr.UnknownValueError:
        print("音声を認識できませんでした。")
        return None
    except sr.RequestError:
        print("音声認識サービスにアクセスできません。")
        return None

def main():
    while True:
        audio_data = record_audio()
        text = recognize_speech(audio_data)
        if text:
            if "おはよう" in text:
                print("「おはよう」が検出されました！音声を再生します。")
                play_audio(MP3_FILE)
            elif "終了" in text:
                print("プログラムを終了します。")
                break
