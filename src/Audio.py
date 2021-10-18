from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import mixer, time
import pyttsx3

mixer.init()

def play_audio_file(audio_file: str, volume: float = 1.0, wait_for_finish: bool = True) -> None:
    try:
        sound = mixer.Sound(audio_file)
        sound.set_volume(volume)
        channel = sound.play()
        if wait_for_finish:
            while channel.get_busy() == True:
                time.wait(100)
    except FileNotFoundError as e:
        print(f"Could not open file {audio_file}: {e}")

def text_to_speech(text: str) -> None:
    print(f"Saying: {text}")
    ttsengine = pyttsx3.init()
    voices = ttsengine.getProperty('voices')
    ttsengine.setProperty('voice', voices[1].id)
    ttsengine.setProperty('rate', 150) # defaults to 200, sounds rushed
    ttsengine.say(text)
    ttsengine.runAndWait()

def stop_all_sounds() -> None:
    mixer.stop()