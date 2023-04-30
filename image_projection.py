import time
import cv2
import numpy as np

def projectCenter(img1, img2):
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

    # Apply ratio test to filter out good matches
    good_matches = []
    for m in matches:
        if m.distance < 50:
            good_matches.append(m)
    
    good_matches = sorted(good_matches, key=lambda x: x.distance)

    # Extract the matched keypoints from both images
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
    H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Compute the center of the first image
    h, w = img1.shape[:2]
    center = np.float32([[w/2, h/2, 1]])
    center_proj = np.matmul(center, H.T)
    center_proj = center_proj / center_proj[0][2]
    return int(center_proj[0][0]), int(center_proj[0][1])



def printResult(img1, img2, x, y):
    img_proj = cv2.circle(img2, (x, y), 5, (0, 0, 255), -1)
    cv2.imshow('ProjectedImage', img_proj)

    height_camera = img1.shape[0]
    width_camera = img1.shape[1]
    cv2.line(img1, (0, int(height_camera/2)), (width_camera, int(height_camera/2)), (0, 0, 255), 1)
    cv2.line(img1, (int(width_camera/2), 0), (int(width_camera/2), height_camera), (0, 0, 255), 1)

    cv2.imshow('CameraShot', img1)
    time.sleep(2)
    print("Press Key to close Analysis")
    cv2.waitKey(0)
    cv2.destroyWindow('ProjectedImage')
    cv2.destroyWindow('CameraShot')


def cleanup():
    time.sleep(2)
    input("Press Enter to end the program")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
