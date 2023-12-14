import cv2
import mediapipe as mp
import time

# Cargar el modelo de MediaPipe para la detección de manos
mp_hands = mp.solutions.hands # type: ignore
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)  # Cambio aquí

# Función para detectar y dibujar las manos en un frame
def detect_and_draw_hands(frame, is_palm_open, start_time):
    if frame is None:
        print("Empty frame received")
        return is_palm_open, start_time

    # Convertir el fotograma a BGR a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar las manos en el fotograma
    results = hands.process(frame_rgb)

    # Comprobar si se detectaron manos
    if results.multi_hand_landmarks:
        open_palms = 0
        for hand_landmarks in results.multi_hand_landmarks:
            # Aquí chequeamos los puntos de referencia para detectar la palma de la mano
            middle_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]  # type: ignore
            other_fingers_bent = True
            for id, lm in enumerate(hand_landmarks.landmark):
                # Los dedos que no sean el dedo medio están doblados si sus y son mayores que el y del dedo medio
                if id != mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP and lm.y < middle_finger_tip.y:  # type: ignore
                    other_fingers_bent = False
                    break

            # Si la palma de la mano es detectada, incrementar el contador de palmas abiertas
            if other_fingers_bent:
                open_palms += 1

            # Dibujar círculos en los puntos de referencia de la mano
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Si se detectaron dos palmas abiertas y no se ha registrado como abiertas al máximo, actualizar el tiempo de inicio
        if open_palms == 2 and not is_palm_open:
            if start_time == 0:
                start_time = time.time()
            elif time.time() - start_time >= 2:
                is_palm_open = True
        else:
            start_time = 0
            is_palm_open = False

    return is_palm_open, start_time
