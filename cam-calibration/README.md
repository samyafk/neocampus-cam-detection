# Calibration script

The calibration_images-XXX should contain a set of images with a chessboard in different positions and orientations.

To calibrate the camera, run the following command:

```bash
python calibration.py <camera_name> m n width height square_dimension
```

where: 
```
- camera_name: the name of the camera (e.g. bullet, 360, etc.)
- m,n: the number of inner corners in the chessboard (e.g. 9,6)
- width,height: the width and height of the image in pixels (e.g. 1280,720)
- square_dimension: the dimension of the square in the chessboard in mm (e.g. 26.5)
```
## IMPORTANT

The chessboard calibration images should be in `calibration_images-XXX` where `XXX` specifies the camera name.

## Output

The script will output the calibration parameters in the `params-XXX` directory, where `XXX` specifies the camera name.





</br>
</br>
</br>
</br>

# Undistortion script

The images-XXX should contain the images u want to undistort.

To undistort your images, run the following command:

```bash
python undistortion.py <camera_name>
```

where: 
```
- camera_name: the name of the camera (e.g. bullet, 360, etc.)
```
## IMPORTANT BEFORE RUNNING THIS SCRIPT

You should calibrate your camera first using the previous calibration script.

## Output

The script will output the undistorted images in the `results` directory.