#!/usr/bin/env python

import cv2
import numpy as np
import os
import sys

if len(sys.argv) != 4:
    print("Usage: python calibrate.py <image_name> <rows> <cols>\n")
    # Default image
    fname = "image_test2.jpg"
    CHECKERBOARD = (6, 9)
else:
    fname = sys.argv[1]
    CHECKERBOARD = (int(sys.argv[2]), int(sys.argv[3]))

# Defining the dimensions of checkerboard

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = []

# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Get the directory of the current file
curr_path = os.path.dirname(os.path.abspath(__file__))
# Replace backslashes with forward slashes
curr_path = curr_path.replace('\\', '/')
# Create the path to the source image
src_path = curr_path + "/src-images/"
full_path = src_path + fname

img = cv2.imread(full_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Find the chess board corners
# If desired number of corners are found in the image then ret = true
ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

if ret:
    print("Chessboard detected! :)")
else:
    print("Chessboard not detected! :(")

"""
If desired number of corner are detected,
we refine the pixel coordinates and display 
them on the images of checker board
"""
if ret:
    objpoints.append(objp)
    # refining pixel coordinates for given 2d points.
    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    imgpoints.append(corners2)

    # Draw and display the corners
    img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

cv2.imshow('Detected Corners', img)
cv2.waitKey(0)

cv2.destroyAllWindows()

h, w = img.shape[:2]

"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)

# Undistorting the image
dst = cv2.undistort(img, mtx, dist, None, mtx)


# Displaying the undistorted image
cv2.imshow('Calibrated Image', dst)
res_path = curr_path + "/calibrated-images/"
cv2.imwrite(res_path + "calibrated-" + fname, dst)
print("Calibrated image saved in: " + res_path + fname)
cv2.waitKey(0)
cv2.destroyAllWindows()
