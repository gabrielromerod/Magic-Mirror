import cv2
import time
import threading
import queue
from hand_detection import detect_and_draw_hands
from video_handling import load_video, display_frame
from emotions import detect_emotion
from exportador import export_results
from poema import generar_poema
import pygame
from audio import leer_poema
import random
import time


# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Cargar el video
opciones = [1, 2, 3, 4, 5]
random.seed(time.time())

# Configurar la ventana de OpenCV
cv2.namedWindow('Espejo Mágico', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Espejo Mágico', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Bandera para indicar si la palma de la mano está abierta al máximo durante el tiempo suficiente
is_palm_open = False
start_time = 0

# Diccionario para contar las emociones detectadas
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
emotion_counter = {emotion: 0 for emotion in emotion_labels}

# Crear una cola para los resultados de la detección de emociones
emotion_queue = queue.Queue()

# Crear una cola para los fotogramas
frame_queue = queue.Queue(maxsize=1)

def frame_reading_thread(cap, frame_queue):
    while True:
        ret, frame = cap.read()
        if ret:
            frame_queue.put(frame)
        else:
            break

def emotion_detection_thread(frame_queue, emotion_queue):
    while True:
        frame = frame_queue.get()
        emotion, probability = detect_emotion(frame)
        emotion_queue.put((emotion, probability))

# Inicializar el hilo de lectura de fotogramas
frame_thread = threading.Thread(target=frame_reading_thread, args=(cap, frame_queue))
frame_thread.start()

is_video_playing = False
while opciones:  # Mientras haya opciones disponibles
    azar = random.choice(opciones)  # Seleccionar un video al azar
    opciones.remove(azar)  # Eliminar el video seleccionado de las opciones

    video_path = f'videos/video{azar}.mp4'
    audio_path = f'audios/audio{azar}.mp3'
    video_cap, video_size = load_video(video_path)

    while True:
        frame = frame_queue.get()

        if not is_video_playing:
            # Voltear el fotograma horizontalmente para simular un espejo
            frame = cv2.flip(frame, 1)

            is_palm_open, start_time = detect_and_draw_hands(frame, is_palm_open, start_time)

            # Reproducir el audio
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            # Mostrar el fotograma con la detección de la mano
            display_frame('Espejo Mágico', frame)

            # Si la palma de la mano está abierta al máximo, comenzar a reproducir el video
            if is_palm_open and not is_video_playing:
                is_video_playing = True
                video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Comenzar el video desde el principio

                emotion_thread = threading.Thread(target=emotion_detection_thread, args=(frame_queue, emotion_queue,))
                emotion_thread.start()

        else:
            try:
                emotion, probability = emotion_queue.get_nowait()
                if emotion is not None:
                    emotion_counter[emotion] += 1
            except queue.Empty:
                pass

            # Leer y mostrar un fotograma del video
            ret, frame_video = video_cap.read()
            if ret:  # Si se pudo leer un fotograma
                frame_video = cv2.resize(frame_video, video_size)
                display_frame('Espejo Mágico', frame_video)
            else:  # Si no se pudo leer un fotograma, el video ha terminado
                is_video_playing = False
                print("El video ha terminado")
                total = sum(emotion_counter.values())
                if total > 0:  # Para prevenir una división por cero
                    emotion_percentages = {emotion: count / total * 100 for emotion, count in emotion_counter.items()}
                    print("Porcentajes de emoción:", emotion_percentages)
                    poema = generar_poema(emotion_percentages)
                    leer_poema(poema)
                    export_results(video_path, emotion_percentages, poema, audio_path)
                # Limpiar el contador de emociones
                emotion_counter = {emotion: 0 for emotion in emotion_labels}
                is_palm_open = False  # Reiniciar el estado de la mano
                break  # Salir del bucle y comenzar con un nuevo video
                     
        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Al final, liberar la cámara y cerrar todas las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
frame_thread.join()  # Asegurarse de que el hilo de lectura de fotogramas se ha cerrado correctamente

if is_video_playing:  # Si el hilo de detección de emociones se ha iniciado
    emotion_thread.join()  # Asegurarse de que el hilo de detección de emociones se ha cerrado correctamente
