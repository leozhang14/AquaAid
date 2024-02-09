#based on AquaAid.py

import argparse, cv2 as cv, time
def identifyShow(frame):
    frameSet = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameSet = cv.equalizeHist(frameSet)
    # frameSet converts to grayscale for haar cascade to work
    mouths = mouthCascade.detectMultiScale(frameSet)
    for (a,b,c,d) in mouths:
        # building the border of the mouth (detected)
        centre = (a + c//2, b + d//2)
        frame = cv.ellipse(frame, centre, (c//2, d//2), 0, 0, 360, (255, 100, 50), 4)
    cv.imshow('Webcam - AquaAid - Mouth - Press Esc to Quit', frame)
    # webcam caption

# Initializing ArgumentParser object
parser = argparse.ArgumentParser()
# adding arguments to parser
parser.add_argument('--mouth_cascade', help='path to haarcascade database (mouth)', default='data/haarcascade_mcs_mouth.xml')
parser.add_argument('--camera', help='webcam', type=int, default=0)
# Parsing the CLI commands
args = parser.parse_args()
pathName = args.mouth_cascade

# creating instance of CascadeClassifier in cv module
mouthCascade = cv.CascadeClassifier()

if not mouthCascade.load(cv.samples.findFile(cv.data.haarcascades + 'haarcascade_mcs_mouth.xml')):
    exit(0)
cameraIdx = args.camera
vidCapture = cv.VideoCapture(cameraIdx)
# vidCapture is a video capture object
if not vidCapture.isOpened:
    exit(0)
while True:
    foo, display = vidCapture.read()
    # where foo is string
    if display is None:
        break
    #isDrinking = True
    #if isDrinking == True:
        #print("--- %s seconds ---" % round((time.time() - start_time), 3))
    #else:
        #start_time = time.time()
    identifyShow(display)
    stopCheck = cv.waitKey(10) & 0xff
    if stopCheck == 27:
        break