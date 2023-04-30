import time
import cv2
import trigger

CAMERA = 1
print("Waiting for camera start...")
vid = cv2.VideoCapture(CAMERA)
print("Camera start complete")


def adjustTarget():
    time.sleep(2)
    print("This Window is to adjust the Camera")
    print("Click Press the 'f' Key when you're done to close this window and start...")
    while(True):
        ret, frame = vid.read()
        height_camera = frame.shape[0]
        width_camera = frame.shape[1]
        cv2.line(frame, (0, int(height_camera/2)), (width_camera, int(height_camera/2)), (0, 0, 255), 1)
        cv2.line(frame, (int(width_camera/2), 0), (int(width_camera/2), height_camera), (0, 0, 255), 1)

        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('f'):
            cv2.destroyWindow('frame')
            return frame

def cameraShot():
    trigger.detectKeyTrigger()
    ret, frame = vid.read()
    return frame
