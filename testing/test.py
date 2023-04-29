import cv2

cap = cv2.VideoCapture(1)  # 0 is the index of the camera
ret, camera_image = cap.read()


from PIL import ImageGrab

screen_image = ImageGrab.grab()


import numpy as np
import cv2

# Convert both images to grayscale
camera_gray = cv2.cvtColor(camera_image, cv2.COLOR_BGR2GRAY)
screen_gray = cv2.cvtColor(np.array(screen_image), cv2.COLOR_BGR2GRAY)

# Create ORB detector and compute keypoints and descriptors for both images
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(camera_gray, None)
kp2, des2 = orb.detectAndCompute(screen_gray, None)

# Create a Brute-Force Matcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match the keypoints from both images
matches = bf.match(des1, des2)

# Sort the matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# Draw the matches on the screen image
result = cv2.drawMatches(camera_gray, kp1, screen_gray, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
 

cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
