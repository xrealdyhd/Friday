import speech_recognition as sr
import pyttsx3
import subprocess
import requests
import time
from datetime import datetime
import os

nircmd_path = r"C:\nircmd.exe"

commands = {
    "not defteri": r"notepad.exe",
    "spotify": r"C:\Users\xRealdyHD\AppData\Roaming\Spotify\Spotify.exe",
    "discord": r"C:\Users\xRealdyHD\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "tarayıcı": r"C:\Users\xRealdyHD\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe",
    "hesap makinesi": r"calc.exe",
    "bilgisayarı kapat": r"shutdown /s /f /t 0"
}

relay_commands = {
    "open the light": "on",
    "close the light": "off"
}

door_commands = {
    "open the door": "on",
}

ses = {
    "sesi fulle": "65535",
    "sesi kapat": "-65535",
    "sesi 1 arttır": "655",
    "sesi 5 arttır": "3275",
    "sesi 10 arttır": "6550",
    "sesi 20 arttır": "13100",
    "sesi 1 azalt": "-655",
    "sesi 5 azalt": "-3275",
    "sesi 10 azalt": "-6550",
    "sesi 20 azalt": "-13100",

}

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    r.adjust_for_ambient_noise(source)

engine = pyttsx3.init()


def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def listen_for_command():
    with mic as source:
        audio = r.listen(source)
        text = r.recognize_google(audio, language='tr-TR').lower()
        print("Detected Command: " + text)
        return text


awake = False
first_run = True

while True:
    try:
        if first_run:
            first_run = False
            speak("System Starting...")
            time.sleep(0.5)
            speak("System Opening...")

        if not awake:
            with mic as source:
                audio = r.listen(source)
                text = r.recognize_google(audio, language='tr-TR').lower()

                if "friday" in text:
                    awake = True
                    speak("Yes Boss.")
                else:
                    print("Friday İs Sleeping...")
                    continue

        else:
            command = listen_for_command()

            if "what is my name" in command:
                speak("Your name is Yiğit Eren.")
                awake = False

            elif "restart" in command:
                speak("Ok Boss system restarting...")
                time.sleep(2)
                first_run = True
                awake = False

            elif "can you hear me" in command:
                speak("Yes Boss i can hear you.")
                awake = False

            elif "don't listen" in command:
                speak("Ok Boss i don't listen")
                awake = False

            elif "what time is it" in command:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                speak(f"The current time is {current_time}")
                awake = False


            else:
                command_found = False
                for keyword, cmd in commands.items():
                    if keyword in command:
                        speak("Okay Boss.")
                        os.system(cmd)
                        command_found = True
                        awake = False
                        break

                for keyword, state in relay_commands.items():
                    if keyword in command:
                        url = f"http://192.168.1.97/{state}"
                        response = requests.get(url)
                        speak(f"Okay Boss.")
                        awake = False
                        command_found = True

                for keyword, durum in ses.items():
                    if keyword in command:
                        subprocess.run([nircmd_path, "changesysvolume", durum])
                        speak(f"Okay Boss.")
                        awake = False
                        command_found = True

                if not command_found:
                    speak("I did not understand your command")

    except:
        pass
