# python hand_recognize.py --bounding-box "10,350,225,590"

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from sklearn.metrics import pairwise
import numpy as np
import argparse
import imutils
import time
import cv2
import os

# Motion Detector class to detect hand
class MotionDetector:
    def __init__(self, accumWeight = 0.5):
        # store the accumulated weight factor
        self.accumWeight = accumWeight

        # initialize the background model
        self.bg = None
        
    def update(self, image):
        # if the background model is None, initialize it
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        # update the background model by accumulating the weighted average
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)
        
    def detect(self, image, tVal=25):
        # compute the absolute difference between the background model and the image
        # passed in, then threshold the delta image
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        # if no contours were found, return None
        if len(cnts) == 0:
            return None

        # otherwise, return a tuple of the thresholded image along with the contour area
        return (thresh, max(cnts, key=cv2.contourArea))

# Gesture Detector class to differ gesture used
class GestureDetector:
    def __init__(self):
        pass

    def detect(self, thresh, cnt):
        # compute the convex hull of the contour and then find the extreme most points along
        # the hull
        hull = cv2.convexHull(cnt)
        extLeft = tuple(hull[hull[:, :, 0].argmin()][0])
        extRight = tuple(hull[hull[:, :, 0].argmax()][0])
        extTop = tuple(hull[hull[:, :, 1].argmin()][0])
        extBot = tuple(hull[hull[:, :, 1].argmax()][0])

        # compute the center (x, y)-coordinates based on the extreme points, then add a little
        # extra percentage to the y-coordinate to lower the region towards the center of the
        # palm
        cX = (extLeft[0] + extRight[0]) / 2
        cY = (extTop[1] + extBot[1]) / 2
        cY += (cY * 0.15)
        cY = int(cY)

        # compute the distances between the centroid and the extreme coordinates, then find the
        # largest distance, and use it to complete radius of palm region
        D = pairwise.euclidean_distances([(cX, cY)], Y=[extLeft, extRight, extTop, extBot])[0]
        maxDist = D[D.argmax()]
        r = int(0.7 * maxDist)
        circum = 2 * np.pi * r

        # construct the circular ROI that includes the palm + fingers
        circleROI = np.zeros(thresh.shape[:2], dtype="uint8")
        cv2.circle(circleROI, (cX, cY), r, 255, 1)
        circleROI = cv2.bitwise_and(thresh, thresh, mask=circleROI)

        # find contours in the circular ROI and initialize the total number of fingers counted
        # in the frame
        cnts = cv2.findContours(circleROI.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
        total = 0

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)

            # increment the total number of fingers only if (1) the number of points along the
            # contour does not exceed 25% of the circumfrence and (2) the contour region is not
            # at the bottom of the circle (which is the wrist area)
            if c.shape[0] < circum * 0.25 and (y + h) < cY + (cY * 0.25):
                total += 1

        # return the total number of fingers detected
        return total

    @staticmethod
    def drawText(roi, i, val, color=(0, 0, 255)):
        # draw the text on the ROI
        cv2.putText(roi, str(val), ((i * 50) + 20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
            color, 3)
        print values[0]
        if values[0]  == 1:
            cv2.putText(roi, "Display time", (90, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                color, 3)
            os.system("sudo python time_display.py")
        elif values[0]  == 2:
            cv2.putText(roi, "Weather report", (90, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                color, 3)
            os.system("sudo python weather_report5.py")
        elif values[0]  == 3:
            cv2.putText(roi, "Calendar events", (90, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                color, 3)
            os.system("sudo python quickstart5.py")
        elif values[0]  == 4:
            cv2.putText(roi, "Music player", (90, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                color, 3)
            os.system("python MusicPlayer.py")
        elif values[0]  == 5:
            cv2.putText(roi, "Ending", (90, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                color, 3)
            os.system("sudo python end.py")

    @staticmethod
    def drawBox(roi, i, color=(0, 0, 255)):
        # draw the box on the ROI
        cv2.rectangle(roi, ((i * 50) + 10, 10), ((i * 50) + 50, 60), color, 2)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--bounding-box", required=True,
        help="comma separted list of top, right, bottom, left coordinates of hand ROI")
ap.add_argument("-v", "--video", required=False, help="path to the (optional) video file")
args = vars(ap.parse_args())

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print "[INFO] warming up..."
time.sleep(2)

# unpack the hand ROI, then initialize the motion detector and gesture detector
(top, right, bot, left) = np.int32(args["bounding_box"].split(","))
gd = GestureDetector()
md = MotionDetector()

# initialize the total number of frames read thus far, a bookkeeping variable used to
# keep track of the number of consecutive frames a gesture has appeared in, along
# with the values recognized by the gesture detector
numFrames = 0
gesture = None
values = []

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image and initialize
    # the timestamp and occupied/unoccupied text    
    frame = f.array

    # resize the frame and flip it so the frame is no longer a mirror view
    frame = imutils.resize(frame, width=600)
    frame = cv2.flip(frame, 1)
    clone = frame.copy()
   
    # extract the ROI, passing in right:left since the image is mirrored, then
    # blur it slightly
    roi = frame[top:bot, right:left]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # if we not reached 32 initial frames, then calibrate the skin detector
    if numFrames < 32:
        md.update(gray)
    elif numFrames == 32:
        print "[INFO] background received..."
    # otherwise, detect skin in the ROI
    else:
        # detect motion (i.e., skin) in the image
        skin = md.detect(gray)

        # check to see if skin has been detected
        if skin is not None:
            # unpack the tuple and draw the contours on the image
            (thresh, c) = skin
            cv2.drawContours(clone, [c + (right, top)], -1, (0, 255, 0), 2)
            fingers = gd.detect(thresh, c)

            # if the current gesture count is None, initialize it
            if gesture is None:
                gesture = [1, fingers]

            # otherwise the finger count has been initialized
            else:
                # if the finger counts are the same, increment the number of frames
                if gesture[1] == fingers:
                    gesture[0] += 1

                    # if we have reached a sufficient number of frames, draw the number of the
                    # screen
                    if gesture[0] >= 25:
                        # if the values list is already full, reset it
                        if len(values) == 1:
                            values = []

                        # update the values list and reset the gesture
                        values.append(fingers)
                        gesture = None

                # otherwise, the finger counts do not match up, so reset the bookkeeping variable
                else:
                    gesture = None

    # check to see if there is at least one entry in the values list
    if len(values) > 0:
        # draw the first digit and the plus sign
        GestureDetector.drawBox(clone, 0)
        GestureDetector.drawText(clone, 0, values[0])
        values = []
        
    # draw the hand ROI and increment the number of processed frames
    cv2.rectangle(clone, (left, top), (right, bot), (0, 0, 255), 2)
    numFrames += 1

    # show the frame to our screen
    cv2.imshow("Frame", clone)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

            
    
