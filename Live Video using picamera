# -*- coding: utf-8 -*-ç
# This program illustrates how to capture frames in a video stream and how to do further processing on them
# It uses numpy to do the calculations and OpenCV to display the frames

import picamera
import picamera.array                          # This needs to be imported explicitly
import time
import cv2
import numpy as np                              


# Initialize the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = True                       # Flip upside down or not
camera.hflip = True                             # Flip left-right or not


# Create a data structure to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))


# Allow the camera to warm up
time.sleep(0.1)

# Main program 
try:
        
    # Continuously capture frames from the camera
    # Each rawframe is accessible as ´frame´ inside the for-loop
    # Note that the format is BGR instead of RGB because we want to use openCV later on and it only supports BGR
    for frame in camera.capture_continuous(rawframe, format = 'bgr', use_video_port = True):

        # Clear the rawframe in preparation for the next frame
        # Do not modify this line of code
        rawframe.truncate(0)


        # Create a numpy array representing the image
        # Do not modify this line of code
        image = frame.array


        #-----------------------------------------------------
        # We will use numpy to do our image manipulations
        #-----------------------------------------------------

        # Make a copy of the image
        image2 = image.copy()
        image2.setflags(write=1)                                   # Making the array mutable                                                                                                      

        # Modify the copy of the image
        # This is where you would write your code to manipulate the image (invert it, make it grayscale, etc.)
        # Remember: images are stored as BGR
        # Show the frames
        cv2.imshow("Orignal frame", image)
            
        # The waitKey command is needed to force openCV to show the image
        cv2.waitKey(1)


# Reset by pressing CTRL + C
except KeyboardInterrupt:
        print("Program stopped by User")
        cv2.destroyAllWindows()
        # Clean up the camera resources
        camera.close()
        

