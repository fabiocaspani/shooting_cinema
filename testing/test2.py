import datetime
import win32api
import win32gui
import win32ui
import win32con
import cv2
import numpy as np
from PIL import ImageGrab

# Get the dimensions of the primary display
width_screen = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
height_screen = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

# Create a device context (DC) object for the full-screen window
hdesktop = win32gui.GetDesktopWindow()
desktop_dc = win32gui.GetWindowDC(hdesktop)
dc = win32ui.CreateDCFromHandle(desktop_dc)

# Create a memory DC object for the screenshot
mem_dc = dc.CreateCompatibleDC()

# Create a bitmap object for the screenshot
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(dc, width_screen, height_screen)
mem_dc.SelectObject(screenshot)


# define a video capture object
vid = cv2.VideoCapture(1)

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
        break

print(datetime.datetime.now())
img1 = frame


print(datetime.datetime.now())
mem_dc.BitBlt((0, 0), (width_screen, height_screen), dc, (0, 0), win32con.SRCCOPY)
print(datetime.datetime.now())

# Convert the bitmap to an image usable with OpenCV
bmpinfo = screenshot.GetInfo()
img2 = np.frombuffer(screenshot.GetBitmapBits(True), dtype='uint8')
img2.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)


mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())

#img2 = np.array(ImageGrab.grab())

# Compute the centers of the images
h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]
center1 = np.float32([w1/2, h1/2]).reshape(-1, 1, 2)
center2 = np.float32([w2/2, h2/2]).reshape(-1, 1, 2)

# Initialize the ORB detector and brute force matcher
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Detect ORB features and compute descriptors for each image
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Match the descriptors using brute force matching
matches = bf.match(des1, des2)

matches = sorted(matches, key=lambda x: x.distance)

# Apply ratio test to filter out good matches
good_matches = []
for m in matches:
    if m.distance < 50:
        good_matches.append(m)

print(len(good_matches))
print(len(matches))

# Extract the matched keypoints from both images
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Compute the center of the first image
h, w = img1.shape[:2]
center = np.float32([[w/2, h/2, 1]])
center_proj = np.matmul(center, H.T)
center_proj = center_proj / center_proj[0][2]
print(center_proj)

# Draw a circle at the projected center in the second image
img2_proj = cv2.circle(img2, (int(center_proj[0][0]), int(center_proj[0][1])), 5, (0, 0, 255), -1)
cv2.imshow('Projected Image', img2_proj)
cv2.waitKey(0)
cv2.destroyAllWindows()
