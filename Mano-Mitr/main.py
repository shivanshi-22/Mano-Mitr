from keras.models import load_model
from time import sleep, time
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier(r'Emotion_Detection_CNN-main\haarcascade_frontalface_default.xml')
classifier = load_model(r'Emotion_Detection_CNN-main\model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)

start_time = time()
duration = 30  # duration for capturing frames (in seconds)
depressed_count = 0
not_depressed_count = 0

while time() - start_time < duration:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            prediction = classifier.predict(roi)[0]
            if prediction.argmax() in [3, 4, 6]:  # Happy, Neutral, Surprise
                label = "Not Depressed"
                not_depressed_count += 1
            else:
                label = "Depressed"
                depressed_count += 1

            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Calculate and display the result
total_frames = depressed_count + not_depressed_count
depressed_percentage = (depressed_count / total_frames) * 100
not_depressed_percentage = (not_depressed_count / total_frames) * 100
print("Total Frames: ", total_frames)
print("Depressed Frames: ", depressed_count, f"({depressed_percentage:.2f}%)")
print("Not Depressed Frames: ", not_depressed_count, f"({not_depressed_percentage:.2f}%)")

cap.release()
cv2.destroyAllWindows()
