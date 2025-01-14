import cv2
import collections

camera = cv2.VideoCapture(0)

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('lbph_classifier.yml')

height, width = 220, 220
recent_predictions = collections.deque(maxlen=5)  # Suavização dos resultados
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

while True:
    ok, frame = camera.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)  # Normaliza a iluminação
    detections = detector.detectMultiScale(img, scaleFactor=1.2, minNeighbors=7, minSize=(100, 100))

    for (x, y, w, h) in detections:
        img_face = cv2.resize(img[y:y + h, x:x + w], (width, height))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label, confidence = recognizer.predict(img_face)

        name = "Desconhecido"
        if confidence < 70:
            recent_predictions.append(label)
            most_common_label = max(set(recent_predictions), key=recent_predictions.count)

            if most_common_label == 1:
                name = "Amanda"
            elif most_common_label == 2:
                name = "Fernando"

        cv2.putText(frame, name, (x, y + h + 30), font, 2, (0, 255, 0), 2)

    cv2.imshow('Face', frame)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
