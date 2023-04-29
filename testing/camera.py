# import the opencv library
import cv2
  
  
# define a video capture object
vid = cv2.VideoCapture(1)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    
    # Drawing the lines
    height = frame.shape[0]
    width = frame.shape[1]
    cv2.line(frame, (0, int(height/2)), (width, int(height/2)), (0, 0, 255), 1)
    cv2.line(frame, (int(width/2), 0), (int(width/2), height), (0, 0, 255), 1)

    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()