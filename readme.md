# SUMO Hackathon - SumoWrestlers
## Project Description:
An automatic household light switch system using a camera sensor thing for households with a congenitally blind member

## Current Project Progress
### faceRecog.py
Currently is able to look for people through a webcam and can track people coming in and out of the main door. It would also be able to control a LED which can be later changed to the light system in the house. 

### faceTrainer.py
Currently empty but it should be able to learn to recognize a face and save it in trainingdata.yml. 

### centroidtracker.py
Tracker class retrieved from https://github.com/Neoanarika/object-tracking-detection


### data/haarcascades
Training data retrieved from https://github.com/opencv/opencv/tree/master/data


## Bibliography
Aswinth, R(2019) Real Time Face Recognition with Raspberry Pi and OpenCV [Computer Program]. https://circuitdigest.com/microcontroller-projects/raspberry-pi-and-opencv-based-face-recognition-system

Neoanarika(2019) object-tracking-detection [Source Code] https://github.com/Neoanarika/object-tracking-detection

OpenCV(n.d) Cascade Classifier [Computer Program]. https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html

