from deepface import DeepFace
import cv2
from catalog.models import MediaFile
import os
from django.conf import settings
import dlib

def analize_emotions(file:MediaFile):
    media_path = os.path.join(settings.MEDIA_ROOT, 'results', file.file_name)
    os.makedirs(os.path.dirname(media_path), exist_ok=True)

    img_path = file.start_file
    data = DeepFace.analyze(img_path=img_path.path, actions=["emotion","age","race","gender"],detector_backend="retinaface")


    image = cv2.imread(img_path.path)


    if not isinstance(data, list):
        data= [data]


    for i,result in enumerate(data):
        region = result['region']
        x, y, w, h = region['x'], region['y'], region['w'], region['h']
        emotion = result['dominant_emotion']

        # Рисуем рамку
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        confidence = result['emotion'][emotion]
        label = f"face {i+1}"
        data[i]['Id']=i+1
        text_y = y - 10 if y - 10 > 10 else y + 20
        cv2.putText(image, label, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.putText(image, f"{emotion}: {confidence:.2f}%", (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0),
                    2)
    print(data)
    cv2.imwrite(media_path, image)
    return {'media_path':media_path,'data':data}

def analize_landmarks(file:MediaFile):
    media_path = os.path.join(settings.MEDIA_ROOT, 'landmarks', file.file_name)
    os.makedirs(os.path.dirname(media_path), exist_ok=True)


    detector = dlib.get_frontal_face_detector()

    predictor_path = os.path.join(settings.BASE_DIR, "static", "shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)

    img=file.start_file
    image = cv2.imread(img.path)

    # Преобразуем изображение в черно-белое
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Детекция лиц
    faces = detector(gray)

    for face in faces:
        x1, y1, x2, y2 = (face.left(), face.top(), face.right(), face.bottom())
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        # Глаза
        for n in range(36, 48):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
        # Брови
        for n in range(17, 27):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (255, 0, 0), -1)
        # Подбородок
        for n in range(5, 12):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (0, 255, 255), -1)
        #нос
        for n in range(27, 36):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (255, 255, 255), -1)
        #рот
        for n in range(48, 68):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (0,0,0), -1)

    cv2.imwrite(media_path, image)
    return {'media_path':media_path}
#analize_landmarks()