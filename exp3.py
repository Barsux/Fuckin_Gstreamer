import time
import cv2

# Cam properties
fps = 24
frame_width = 640
frame_height = 360
# Create capture
cap = cv2.VideoCapture("test.mp4")
# Define the gstreamer sink
gst_str_rtp = "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5000"


# Check if cap is open
if cap.isOpened() is not True:
    print ("Cannot open camera. Exiting.")
    quit()

# Create videowriter as a SHM sink
out = cv2.VideoWriter(gst_str_rtp, 0, fps, (frame_width, frame_height), True)

# Loop it
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('Frames', frame)
    #out.write(frame)

cap.release()