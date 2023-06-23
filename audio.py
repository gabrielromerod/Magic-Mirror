from gtts import gTTS
import os
import pygame

def leer_poema(poema):
    tts = gTTS(text=poema, lang='es')
    tts.save("poema.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("poema.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Controla la velocidad de reproducción

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    os.remove("poema.mp3")
