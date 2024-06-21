import cv2 as cv
import matplotlib.pyplot as plt
import pickle
import os
import sys
from mapping import transform_point
import folium


# Check if the number of arguments is correct
if len(sys.argv) != 3:
    print("Please check the README for more information on the usage of the Homography script.")
    sys.exit()
else:
    camera_name = sys.argv[1]
    camera_img_name = sys.argv[2]

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

# Verify that the images were loaded correctly
if img_cam is None:
    print("Error while loading the images")
    exit()



while True:
    # Afficher l'image source
    plt.figure(figsize=(12, 6))
    
    # Afficher l'image source
    plt.imshow(cv.cvtColor(img_cam, cv.COLOR_BGR2RGB))
    plt.title('Cliquez pour sélectionner un point')
    
    # Sélectionner un point sur l'image source
    points = plt.ginput(1, timeout=-1)  # Timeout=-1 pour attendre indéfiniment un clic
    plt.close()
    
    if len(points) == 0:
        break

    point = points[0]
    transformed_point = transform_point(point, H)
    
    latitude = transformed_point[0][0]
    longitude = transformed_point[1][0]
    print("Le point selectionné est à {}, {}".format(latitude, longitude))
    
    esri_tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    # Create a map centered around the given latitude and longitude
    m = folium.Map(location=[latitude, longitude], zoom_start=19, tiles=esri_tiles, attr='Esri')
    # Add a marker to the map
    # folium.Marker([latitude, longitude], popup='Location').add_to(m)
    radius = 2
    folium.Circle(
        location=[latitude, longitude],
        radius=radius,
        color="black",
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color="yellow",
        fill=False,  # gets overridden by fill_color
        popup="{} meters".format(radius),
        tooltip="Coucou!",
    ).add_to(m)
    m
    # Save the map as an HTML file
    m.save("map.html")

    plt.figure(figsize=(12, 6))
    plt.imshow(cv.cvtColor(img_cam, cv.COLOR_BGR2RGB))
    plt.title('Image Source')
    plt.scatter(point[0], point[1], color='red')
    plt.show()
    

    
