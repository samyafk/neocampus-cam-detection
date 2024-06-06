# Homography script

This script allows to map pixel coordinates to real world coordinates using a homography matrix.

## Usage

```bash
python homography.py <camera_name> <camera_image> <map_image>
```

- `camera_name`: Name of the camera (e.g. `bullet`, `360`)
- `camera_image`: Name of the image taken by the camera
- `map_image`: Name of the map image


## IMPORTANT BEFORE RUNNING THE SCRIPT

- Make sure that the camera image and the map image are in the `images` folder
- Make sure to run the calibration script before running this script
- Make sure that the camera images are already undistorted


## Output

This script will output the homography matrix in the `params-XXX` folder. The `XXX` is the camera name.

<br/>
<br/>
<br/>
<br/>



# Mapping-test script

This allows you to test the mapping of pixel coordinates to real world coordinates using the homography matrix.

## Usage

```bash
python mapping-test.py <camera_name> <camera_image> <map_image>
```

# IMPORTANT BEFORE RUNNING THE SCRIPT

- Make sure that the undistorted camera image and the map image are in the `images` folder
