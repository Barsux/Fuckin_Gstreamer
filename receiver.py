import cv2, threading, uvicorn
from fastapi import FastAPI
global video_frame
video_frame = None

cv2.namedWindow('stream')

# Use locks for thread-safe viewing of frames in multiple browsers
# locks prevent the program from getting user inputs from multiple sources
# lock helps syncronize the program
global thread_lock
thread_lock = threading.Lock()

app = FastAPI()


def main():
    global video_frame
    camSet = 'udpsrc host=0.0.0.0 port=8000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, \
        encoding-name=(string)H264,\
         payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink'
    video_capture = cv2.VideoCapture(camSet, cv2.CAP_GSTREAMER)  # initalizes our video feed
    # video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 0)#sets camera buffer to 0 meaning we wont get double frames
    print("reading frames")

    while True:

        ret, frame = video_capture.read()

        if not ret:
            print('empty frame')
            break

        cv2.imshow(frame, 'stream')
        # with thread_lock:
        #     video_frame = frame.copy()


def encodeFrame():  # encode frame function takes the frames and encoding them to jpg and encodes them again to bytes so we can stream them
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        # Output image as a byte array
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded_image) + b'\r\n')


@app.get("/")
async def video_feed():  # our stream function, streams the frames encodeFrame has made to the IP and port we chose
    return StreamingResponse(encodeFrame(), media_type="multipart/x-mixed-replace;boundary=frame")


if __name__ == '__main__':
    # Create a thread and attach the method that captures the image frames, to it
    process_thread = threading.Thread(target=main)

    # Start the thread
    process_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=9000, access_log=True)