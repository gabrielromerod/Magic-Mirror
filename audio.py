from gtts import gTTS
import os

def leer_poema(poema):
    tts = gTTS(text=poema, lang='es')
    tts.save("poema.mp3")
