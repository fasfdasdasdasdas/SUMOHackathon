import cv2 as cv
import imutils
import argparse
from centroidtracker import CentroidTracker
from gpiozero import LED

# Declaring Variables
OwnerHome = False

parser = argparse.ArgumentParser(description='Arguments parsed')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera1', help='EnterCam', type=int, default=0)
parser.add_argument('--camera2', help='ExitCam', type=int, default=1)
parser.add_argument('--LEDno', help= "LightControl", type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

# Loading Recognizer and the trainer 
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('trainingdata.yml')

# Load Tracker and LED
trackerFront = CentroidTracker()
trackerBack = CentroidTracker()
led = LED(args.LEDno)

# Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

camera_device_front = args.camera1
# Read the video stream 
cap = cv.VideoCapture(camera_device_front)

camera_device_back = args.camera2
cap_back = cv.VideoCapture(camera_device_back)
if not cap.isOpened or not cap_back.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

while True:
    rect_front = []
    # Door Capture Enter
    ret, frame = cap.read()

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    # Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        rect_front.append(center)
        # In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
        
        #Try to recognize faces
        id, confidence = recognizer.predict(faceROI)
        if (confidence < 80): # Visitor when confidence less than 80
            trackerFront.register(center)
        else: # Else it is the owner entering the home
            OwnerHome = True


    # Door capture exit
    ret_back, frame_back = cap_back.read()
    rect_back = []

    frame_gray_back = cv.cvtColor(frame_back, cv.COLOR_BGR2GRAY)
    frame_gray_back = cv.equalizeHist(frame_gray)

    # Detect faces
    faces_back = face_cascade.detectMultiScale(frame_gray_back)
    for (x,y,w,h) in faces_back:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame_back, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        rect_back.append(center)
        # In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
        
        #Try to recognize faces
        id, confidence = recognizer.predict(faceROI)
        if (confidence < 80): # Visitor when confidence less than 80
            trackerBack.register(center)
        else: # Else it is the owner entering the home
            OwnerHome = False
    

    # Update tracking of people
    peopleIn = trackerFront.update(rect_front)
    peopleOut = trackerBack.update(rect_back)
    if (peopleIn-peopleOut == 0) or OwnerHome == False:
        led.off()
    else:
        led.on()
