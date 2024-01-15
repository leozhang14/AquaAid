from __future__ import print_function
import cv2 as cv
import argparse
import time


def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect face
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
    cv.imshow('Capture - Face detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascade_frontalface_alt.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
face_cascade = cv.CascadeClassifier()
#-- 1. Loading cascades
if not face_cascade.load(cv.samples.findFile(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')):
    print('--(!)Error loading face cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read webcam stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    #isDrinking = True
    #if isDrinking == True:
        #print("--- %s seconds ---" % round((time.time() - start_time), 3))
    #else:
        #start_time = time.time()
    detectAndDisplay(frame)
    stopProcess = cv.waitKey(10) & 0xff
    if stopProcess == 27:
        break