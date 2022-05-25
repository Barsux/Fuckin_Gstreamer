import time
import cv2
VIDEO_FILE = ""
fps = 24/1
frame_width = 640
frame_height = 360
flip = 0
cam, out = None, None
def init() -> tuple:
    global cam, out
    cam = cv2.VideoCapture("test.mp4")
    if not cam.isOpened():
        return (-1, "Сука файла нету")
    out = cv2.VideoWriter("appsrc ! autovideosink", cv2.CAP_GSTREAMER, 0, 24, (320, 280), True)
    if not out.isOpened():
        #return (-1, "Сука пайплайна нету")
        pass
    return (1, "")

def loop() -> None:
    while cam.isOpened():
        ret, frame = cam.read()
        cv2.imshow('Frames', frame)
        out.write(frame)
        if cv2.waitKey(1) == ord('q'):
            break

def main():
    status, error = init()
    if(status < 0):
        print(error)
        print("Не работает нихуя!")
        return
    loop()
    cam.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()