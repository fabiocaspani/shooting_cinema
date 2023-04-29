import cv2
import trigger

CAMERA = 1
print("wait for camera start")
vid = cv2.VideoCapture(CAMERA)
print("Camera start complete")


def adjustTarget():
# define a video capture object
    while(True):
        
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        
        # Drawing the lines
        height_camera = frame.shape[0]
        width_camera = frame.shape[1]
        cv2.line(frame, (0, int(height_camera/2)), (width_camera, int(height_camera/2)), (0, 0, 255), 1)
        cv2.line(frame, (int(width_camera/2), 0), (int(width_camera/2), height_camera), (0, 0, 255), 1)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('p'):
            return frame

def cameraShot():
    trigger.detectTrigger()
    ret, frame = vid.read()
    return frame
