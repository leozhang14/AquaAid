# To be implemented:

import time
#isDrinking = True
    #if isDrinking == True:
        #print("--- %s seconds ---" % round((time.time() - start_time), 3))
    #else:
        #start_time = time.time()

import cv2 as cv
import datetime
# from AquaAid import identifyShow

def detect_color_in_roi(frame, roi_coords, color_to_detect):
    """
    Detects if the specified color is present in the given frame.
    If the color is detected, returns the timestamp; otherwise, returns None.
    ** Note to change so that it its live, not static.
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


def hydrate_logic(time_opened):
    # need to add initial parameter, then take difference between timestamps
    # idea:
        # return final - initial (in seconds)
    # Example: return the length of the timestamp string - to be refactored
    return len(time_opened)

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

# Define the color to detect (in BGR format)
color_to_detect = (255, 0, 0)

# Initialize variables
time_color_detected = None
running_total = 0

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
    cv.rectangle(frame, (a, b), (c, d), (0, 0, 255), 2)  # Draw rectangle around ROI
    cv.imshow('Color Detection - Esc to Quit', frame)

    # Perform additional logic when the color is first detected
    if time_color_detected:
        value_to_add = hydrate_logic(time_color_detected)
        running_total += int(value_to_add)
        time_color_detected = None  # Reset to None to avoid repeated triggering

    # Break the loop when 'esc' key is pressed
    stopCheck = cv.waitKey(10) & 0xff
    if stopCheck == 27:
        break

# Release the VideoCapture and close all windows
cap.release()
cv.destroyAllWindows()