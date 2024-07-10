# Main

import cv2 as cv
import datetime
import argparse
import sys

# global variables
time_color_detected = None
value_to_add = 0
running_total = 0
# Time duration to volume conversion factor (seconds to milliliters)
timeToVol = 1.265/500
# multiplier derived from human trials

def detect_color_in_roi(frame, roi_coords, color_to_detect):
    """
    Detects if the specified color is present in the given frame.
    If the color is detected, returns the timestamp; otherwise, returns None.
    ** Note to change so that it's live, not static.
    """
    # Extract the frame
    a, b, c, d = roi_coords
    roi = frame[a:c, b:d]

    # Check if the color in the selected area matches the predefined color
    if (roi == color_to_detect).all():
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return timestamp

    return None

def hydrate_logic(initialTime, finTime):
    def timeConvert(stamp):
        return (int(stamp[11]) * 10 * 60 * 60 + int(stamp[12]) * 60 * 60 + int(stamp[14]) * 10 * 60 + int(stamp[15]) * 60
                + int(stamp[17]) * 10 + int(stamp[18]))
    final = timeConvert(finTime)
    initial = timeConvert(initialTime)
    diff = final - initial
    return diff

def outputPrint(total, stream):
    print(total, file=stream)

def enterFrame():
    while True:
        # Capture video frame-by-frame
        ret, frame = cap.read()

        # Display the frame and prompt user to select ROI
        cv.imshow('Choose frame (press Enter)', frame)

        # Break the loop when 'Enter' key is pressed
        if cv.waitKey(1) == 13:
            break
        ### *** Make it reset to initial frame selection


# command line argument for output stream
output_parser = argparse.ArgumentParser(description='Process some data and write output to a file.')
output_parser.add_argument('--output', '-o', type=str,
                    help='Output file path. If not provided, the output will be printed to the console (default stdout).')

output_args = output_parser.parse_args()

# command line arguments for cascade classifier file path and live video input stream
face_parser = argparse.ArgumentParser()
# adding arguments to parser
face_parser.add_argument('--face_cascade', help='path to haarcascade database (front of face)', default='data/haarcascade_frontalface_alt.xml')
face_parser.add_argument('--camera', help='webcam', type=int, default=0)
# Parsing the CLI commands
face_args = face_parser.parse_args()
pathName = face_args.face_cascade

# creating instance of CascadeClassifier in cv module (for local use)
faceCascade = cv.CascadeClassifier()

# Main Process

if not faceCascade.load(cv.samples.findFile(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')):
    exit(0)
cameraIdx = face_args.camera
# Create a VideoCapture object (0 for webcam)
cap = cv.VideoCapture(cameraIdx)

while True:
    # Capture video frame-by-frame
    ret, frame = cap.read()

    # Display the frame and prompt user to select ROI
    cv.imshow('Choose frame (press Enter)', frame)

    # Break the loop when 'Enter' key is pressed
    if cv.waitKey(1) == 13:
        break
# Destroy the window and get the selected area's coordinates (4 values)
cv.destroyAllWindows()
roi_coords = cv.selectROI(frame)
a, b, c, d = map(int, roi_coords)

if cv.waitKey(1) == ord("c"):
    enterFrame()
# Define the color to detect (in BGR format) - based on user input later
color_to_detect = (255, 0, 0)

# Main loop for color detection
while True:
    # Capture video frame-by-frame
    ret, frame = cap.read()

    # Detect color in the specified ROI
    current_time = detect_color_in_roi(frame, (a, b, c, d), color_to_detect)

    # If color is detected, and it's the first time, set the time
    if current_time and time_color_detected is None:
        time_color_detected = current_time

    # Display the frame with the selected ROI
    cv.rectangle(frame, (a, b), (c, d), (0, 0, 255), 3)  # Draw rectangle around ROI
    cv.imshow('Color Detection - Esc to Quit', frame)

    # Perform additional logic when the color is first detected
    if time_color_detected:
        width = float(b) - float(a)
        length = float(d) - float(c)
        area = width * length / 1000
        while cv.waitKey(100) & 0xFF == ord('d'):

            # hold the d key down to produce output - waitKey() to optimize output intervals (how often to display hydration levels)
            value_to_add = int(hydrate_logic(time_color_detected, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) * area)
            running_total += int(value_to_add) * timeToVol

            # Command line argument can be passed to HydrateLogic.py for user to select output filed
            if output_args.output:
                with open(output_args.output, 'w') as output_file:
                    outputPrint(f"Running Total: {running_total} ml", output_file)
            else:
                outputPrint(f"Running Total: {running_total} ml", sys.stdout)

            # for IDE testing - such as PyCharm
            print(f"Running Total: {running_total} ml")

        """"
        
        This is an optional block of code for developer testing to optimize running total (for different devices, water bottles, etc.)
        
        myTime = time.time()
        #Check if 5 seconds have passed since the last print
        if myTime - beginTime >= interval:
            print(f"Running Total: {running_total} ml")
            beginTime = myTime  # Update the start time
        time_color_detected = None  # Reset to None to avoid repeated triggering
        
        """

        # Break the loop when 'esc' key is pressed
        stopCheck = cv.waitKey(1) & 0xff
        if stopCheck == 27:
            break

# Release the VideoCapture and close all windows
cap.release()
cv.destroyAllWindows()