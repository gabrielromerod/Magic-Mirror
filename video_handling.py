import cv2

def load_video(path):
    # Cargar el video con cv2.VideoCapture
    video_cap = cv2.VideoCapture(path)

    # Obtener el tamaño del primer frame del video
    ret, first_frame = video_cap.read()
    video_size = (first_frame.shape[1], first_frame.shape[0])

    return video_cap, video_size


def display_frame(window_name, frame):
    cv2.imshow(window_name, frame)
