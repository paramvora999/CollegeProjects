import cv2
import numpy as np

# Loading the Haar cascade files for face detection and eye detection
f_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_frontalface_default.xml')
e_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_eye.xml')

if f_cascade.empty():
	raise IOError('ERROR')

if e_cascade.empty():
	raise IOError('ERROR')

cap = cv2.VideoCapture(0)

scaling_factor = 0.5

# Iterating until the user hits the 'Esc' key
while True:
    # Capturing the current frame
    _, frame = cap.read()

    frame = cv2.resize(frame, None, fx=ds_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Running the face detector on the grayscale image
    face = f_cascade.detectMultiScale(gray, 1.3, 5)

    # For each face that's detected, running the eye detector
    for (x,y,w,h) in face:
        # Extract the grayscale face ROI
        roi_gray = gray[y:y+h, x:x+w]

        # Extract the color face ROI
        roi_color = frame[y:y+h, x:x+w]

        eye = e_cascade.detectMultiScale(roi_gray)

        # Drawing circles around the eyes
        for (x_eye,y_eye,w_eye,h_eye) in eye:
            center = (int(x_eye + 0.5*w_eye), int(y_eye + 0.5*h_eye))
            radius = int(0.3 * (w_eye + h_eye))
            color = (0, 255, 0)
            thickness = 3
            cv2.circle(roi_color, center, radius, color, thickness)

    # Displaying the output
    cv2.imshow('Eye Detector', frame)

    # Checking if the user hit the 'Esc' key
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()

cv2.destroyAllWindows()
