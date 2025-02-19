import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("話してください...")
        recognizer.adjust_for_ambient_noise(source)  # 周囲のノイズを調整
        audio = recognizer.listen(source)

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

if __name__ == "__main__":
    while True:
        text = recognize_speech()
        if text:
            if "こんにちは" in text:
                response = "こんにちは！元気ですか？"
                print("返答:", response)
                speak(response)
            elif "終了" in text:
                print("プログラムを終了します。")
                break
