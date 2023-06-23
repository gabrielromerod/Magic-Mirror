import cv2
import face_recognition
from keras.models import load_model
import numpy as np

# Cargar el modelo de FER
emotion_model_path = '_mini_XCEPTION.102-0.66.hdf5'
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_target_size = emotion_classifier.input_shape[1:3]

# Las emociones que el clasificador puede predecir
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb, model='hog')
    emotion_text = None
    emotion_probability = None

    for top, right, bottom, left in faces:
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 3)
        
        face = gray[top:bottom, left:right]
        face = cv2.resize(face, (emotion_target_size))
        face = face / 255.0  # normalizar
        face = np.expand_dims(face, 0)  # expandir dimensiones para que se ajuste al formato de entrada del modelo
        face = np.expand_dims(face, -1)  # expandir dimensiones para que se ajuste al formato de entrada del modelo

        emotion_prediction = emotion_classifier.predict(face)[0]
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]

        cv2.putText(frame, emotion_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return emotion_text, emotion_probability

