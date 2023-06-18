import cv2
import time
from hand_detection import detect_and_draw_hands
from video_handling import load_video, display_frame

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

is_video_playing = False
while True:
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

    if is_video_playing:
        # Leer y mostrar un fotograma del video
        ret, frame_video = video_cap.read()
        if ret:  # Si se pudo leer un fotograma
            frame_video = cv2.resize(frame_video, video_size)
            display_frame('Espejo Mágico', frame_video)   
        else:  # Si no se pudo leer un fotograma, el video ha terminado
            is_video_playing = False
            print("El video ha terminado")

    # Salir del bucle si se presiona la tecla 'Esc'
    if cv2.waitKey(1) == 27:
        break

# Liberar los recursos
cap.release()
video_cap.release()
cv2.destroyAllWindows()
