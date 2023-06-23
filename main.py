import cv2
import time
import threading
import queue
from hand_detection import detect_and_draw_hands
from video_handling import load_video, display_frame
from emotions import detect_emotion
from poema import generar_poema

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Cargar el video
video_path = 'video.mp4'
video_cap, video_size = load_video(video_path)

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

def emotion_detection_thread(video_cap, emotion_queue):
    while True:
        ret, frame_video = video_cap.read()
        if ret:
            emotion, probability = detect_emotion(frame_video)
            emotion_queue.put((emotion, probability))
        else:
            break

# Inicializar el hilo de detección de emociones
emotion_thread = threading.Thread(target=emotion_detection_thread, args=(video_cap, emotion_queue,))
emotion_thread.start()

is_video_playing = False
while True:
    if not is_video_playing:
        # Leer el fotograma de la cámara
        ret, frame = cap.read()

        # Voltear el fotograma horizontalmente para simular un espejo
        frame = cv2.flip(frame, 1)

        is_palm_open, start_time = detect_and_draw_hands(frame, is_palm_open, start_time)

        # Mostrar el fotograma con la detección de la mano
        display_frame('Espejo Mágico', frame)

        # Si la palma de la mano está abierta al máximo, comenzar a reproducir el video
        if is_palm_open and not is_video_playing:
            is_video_playing = True
            video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Comenzar el video desde el principio
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
                print(generar_poema(emotion_percentages))
            # Limpiar el contador de emociones
            emotion_counter = {emotion: 0 for emotion in emotion_labels}

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Al final, liberar la cámara y cerrar todas las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
emotion_thread.join()  # Asegurarse de que el hilo de detección de emociones se ha cerrado correctamente
