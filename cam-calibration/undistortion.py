import cv2 as cv
import pickle
import os
import sys
from undistort import undistort_image
import glob

# Check if the number of arguments is correct
if len(sys.argv) != 3:
    print("Please check the README for more information on the usage of the undistortion script.")
    sys.exit()
else:
    camera_name = sys.argv[1]
    image_name = sys.argv[2]

# Get the directory of the current file
curr_path = os.path.dirname(os.path.abspath(__file__))
# Replace backslashes with forward slashes
curr_path = curr_path.replace('\\', '/')
# Create the paths to the source images, results, and parameters
src_path = curr_path + "/images-" + camera_name + "/"
res_path = curr_path + "/results/"
params_path = curr_path + "/params-" + camera_name + "/"

# Check if directory exists
if not os.path.exists(src_path):
    print("The source images directory not found. Please check the README for more information.")

with open(params_path + "dist.pkl", 'rb') as file:
    dist = pickle.load(file)
    
with open(params_path + "cameraMatrix.pkl", 'rb') as file:
    cameraMatrix = pickle.load(file)

images = glob.glob(src_path + "*")
for image in images:
    img = cv.imread(image)
    dst = undistort_image(img, cameraMatrix, dist)
    image_name = image.split("\\")[-1]
    cv.imwrite(res_path + 'undistorted-' + image_name, dst)

