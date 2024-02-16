# To be implemented:

import time
#isDrinking = True
    #if isDrinking == True:
        #print("--- %s seconds ---" % round((time.time() - start_time), 3))
    #else:
        #start_time = time.time()

# Refactor functions and reorganize for more efficient processing

import cv2 as cv
import datetime
# from AquaAid import identifyShow

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

tempInitial = 3*10^-2

def hydrate_logic(initialTime, finTime):
    def timeConvert(stamp):
        return (int(stamp[11]) * 10 * 60 * 60 + int(stamp[12]) * 60 * 60 + int(stamp[14]) * 10 * 60 + int(stamp[15]) * 60
                + int(stamp[17]) * 10 + int(stamp[18]))
    final = timeConvert(finTime)
    initial = timeConvert(initialTime)
    diff = final - initial
    return diff

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

# Create a VideoCapture object (0 for webcam)
cap = cv.VideoCapture(0)

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
color_to_detect = (0, 0, 0)

# Initialize variables
time_color_detected = None
value_to_add = 0
running_total = 0
# Time duration to volume conversion factor (seconds to milliliters)
timeToVol = 1.265/500
# multiplier derived from human trials

#Temp - info for printing intervals, i.e. how often should the volume consumed be displayed to the user
#beginTime = time.time()
#interval = 4  # Print interval in seconds

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
            value_to_add = int(hydrate_logic(time_color_detected, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) * area)
            running_total += int(value_to_add) * timeToVol
            print(f"Running Total: {running_total} ml")

        """""
        This block of code is testing to make the running total print every 3 seconds.
        myTime = time.time()
        #Check if 5 seconds have passed since the last print
        if myTime - beginTime >= interval:
            print(f"Running Total: {running_total} ml")
            beginTime = myTime  # Update the start time
        time_color_detected = None  # Reset to None to avoid repeated triggering
        """


    stopCheck = cv.waitKey(1) & 0xff
    if stopCheck == 27:
        break
    # Break the loop when 'esc' key is pressed

# Release the VideoCapture and close all windows
cap.release()
cv.destroyAllWindows()