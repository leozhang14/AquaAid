# Live feed capture template-base

import argparse, cv2 as cv, time
def identifyShow(frame):
    frameSet = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameSet = cv.equalizeHist(frameSet)
    # frameSet converts to grayscale for haarcascade to work
    faces = faceCascade.detectMultiScale(frameSet)
    for (a,b,c,d) in faces:
        # building the border of the face (detected)
        center = (a + c//2, b + d//2)
        frame = cv.ellipse(frame, center, (c//2, d//2), 0, 0, 360, (255, 100, 50), 4)
    cv.imshow('Webcam - AquaAid - Press Esc to Quit', frame)
    # webcam caption

# Initializing ArgumentParser object for CLI
parser = argparse.ArgumentParser()
# adding arguments to parser
parser.add_argument('--face_cascade', help='path to haarcascade database (front of face)', default='data/haarcascade_frontalface_alt.xml')
parser.add_argument('--camera', help='webcam', type=int, default=0)
# Parsing the CLIs (command-line interfaces)
args = parser.parse_args()
pathName = args.face_cascade

# creating instance of CascadeClassifier in cv module
faceCascade = cv.CascadeClassifier()

if not faceCascade.load(cv.samples.findFile(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')):
    exit(0)
cameraIdx = args.camera
vidCapture = cv.VideoCapture(cameraIdx)
# vidCapture is a video capture object
if not vidCapture.isOpened:
    exit(0)
while True:
    foo, frame = vidCapture.read()
    # where foo is string
    if frame is None:
        break
    #isDrinking = True
    #if isDrinking == True:
        #print("--- %s seconds ---" % round((time.time() - start_time), 3))
    #else:
        #start_time = time.time()
    identifyShow(frame)
    stopCheck = cv.waitKey(10) & 0xff
    if stopCheck == 27:
        break