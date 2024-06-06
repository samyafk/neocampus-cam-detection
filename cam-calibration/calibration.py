import numpy as np
import cv2 as cv
import glob
import pickle
import os
import sys

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

# chessboardSize = (9,6)
# frameSize = (1280,720)
# size_of_chessboard_squares_mm = 26.5

# Check if the number of arguments is correct
if len(sys.argv) != 7:
    print("Please check the README for more information on the usage of the calibration script.")
    sys.exit()
else:
    camera_type = sys.argv[1]
    chessboardSize = (int(sys.argv[2]), int(sys.argv[3]))
    frameSize = (int(sys.argv[4]), int(sys.argv[5]))
    size_of_chessboard_squares_mm = float(sys.argv[6])
    
    


# Get the directory of the current file
curr_path = os.path.dirname(os.path.abspath(__file__))
# Replace backslashes with forward slashes
curr_path = curr_path.replace('\\', '/')
# Create the paths to the source images, results, and parameters
src_path = curr_path + "/calibration_images-" + camera_type + "/"
res_path = curr_path + "/results/"
params_path = curr_path + "/params-" + camera_type + "/"

# Check if directory exists
if not os.path.exists(src_path):
    print("The source images directory not found. Please check the README for more information.")



# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

objp = objp * size_of_chessboard_squares_mm


# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


images = glob.glob(src_path + "*")


for image in images:
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if ret == True:

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(200)
    else:
        print("Chessboard not detected! :(")


cv.destroyAllWindows()


############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

# Check if directory exists, if not, create it
if not os.path.exists(params_path):
    os.makedirs(params_path)

# Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
pickle.dump(cameraMatrix, open( params_path + "cameraMatrix.pkl", "wb" ))
pickle.dump(dist, open( params_path + "dist.pkl", "wb" ))

print("Calibration done! The camera parameters are saved in the corresponding 'params' folder.")


