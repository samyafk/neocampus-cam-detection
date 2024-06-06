import cv2 as cv
import matplotlib.pyplot as plt
import pickle
import os
import sys
from mapping import transform_point


# Check if the number of arguments is correct
if len(sys.argv) != 4:
    print("Please check the README for more information on the usage of the Homography script.")
    sys.exit()
else:
    camera_name = sys.argv[1]
    camera_img_name = sys.argv[2]
    map_img_name = sys.argv[3]

# Get the directory of the current file
curr_path = os.path.dirname(os.path.abspath(__file__))
# Replace backslashes with forward slashes
curr_path = curr_path.replace('\\', '/')
images_path = curr_path + "/images/"
params_path = curr_path + "/params-" + camera_name + "/"


# Loading the homography matrix
with open(params_path + "homographyMatrix.pkl", 'rb') as f:
    H = pickle.load(f)

# Load images
img_cam = cv.imread(images_path + camera_img_name)
img_map = cv.imread(images_path + map_img_name)

# Verify that the images were loaded correctly
if img_cam is None or img_map is None:
    print("Error while loading the images")
    exit()



while True:
    # Afficher l'image source
    plt.figure(figsize=(12, 6))
    
    # Afficher l'image source
    plt.subplot(1, 2, 1)
    plt.imshow(cv.cvtColor(img_cam, cv.COLOR_BGR2RGB))
    plt.title('Cliquez pour sélectionner un point (Image Source)')
    
    # Afficher l'image cible
    plt.subplot(1, 2, 2)
    plt.imshow(cv.cvtColor(img_map, cv.COLOR_BGR2RGB))
    plt.title('Point transformé (Image Cible)')
    
    # Sélectionner un point sur l'image source
    points = plt.ginput(1, timeout=-1)  # Timeout=-1 pour attendre indéfiniment un clic
    plt.close()
    
    if len(points) == 0:
        break

    point = points[0]
    transformed_point = transform_point(point, H)

    # Afficher le point transformé sur l'image cible
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(cv.cvtColor(img_cam, cv.COLOR_BGR2RGB))
    plt.title('Image Source')
    plt.scatter(point[0], point[1], color='red')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv.cvtColor(img_map, cv.COLOR_BGR2RGB))
    plt.title('Image Cible')
    plt.scatter(transformed_point[0], transformed_point[1], color='red')
    
    plt.show()
