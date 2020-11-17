import cv2
import numpy as np

f_cascade = cv2.CascadeClassifier(
        'haar_cascade_files/haarcascade_frontalface_default.xml')

if f_cascade.empty():
	raise IOError('ERROR')

cap = cv2.VideoCapture(0)

s_factor = 0.5

while True:
    _, frame = cap.read()

    frame = cv2.resize(frame, None, 
            fx=s_factor, fy=s_factor, 
            interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_r = f_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in face_r:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

    cv2.imshow('Live Face Detection', frame)

    # Checking if the user hit the 'Esc' key
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()

cv2.destroyAllWindows()
