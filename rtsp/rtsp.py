import cv2
import time
from undistort import undistort_image
import sys
import pickle




# Check if the number of arguments is correct
if len(sys.argv) != 2:
    print("Please check the README for more information on the usage of the undistortion script.")
    sys.exit()
else:
    params_path = sys.argv[1]


with open(params_path + "dist.pkl", 'rb') as file:
    dist = pickle.load(file)
    
with open(params_path + "cameraMatrix.pkl", 'rb') as file:
    cameraMatrix = pickle.load(file)

with open(params_path + "homographyMatrix_gps.pkl", 'rb') as file:
    H = pickle.load(file)

# Define the RTSP stream URL
rtsp_url = "rtsp://cam-91e5:554/profile2/media.smp"

# Measure the start time
start_time_connect = time.time()

# Open the RTSP stream
vcap = cv2.VideoCapture(rtsp_url)

# Measure the end time
end_time_connect = time.time()

# Calculate the connection time
connection_time = end_time_connect - start_time_connect

if not vcap.isOpened():
    print("Error: Unable to open video stream")
    exit()

print(f"Connected to the RTSP stream in {connection_time:.2f} seconds")

# Get the width and height of the frames
fps = int(vcap.get(cv2.CAP_PROP_FPS))

# Define the codec and create a VideoWriter object
# 'XVID' is the codec. You can use other codecs like 'MJPG', 'X264', etc.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = '15_sec_cam_test.avi'

ret, frame = vcap.read()
if not ret:
    print("Error: Unable to read frame from video stream")
    vcap.release()
    exit()

corrected_frame = undistort_image(frame, cameraMatrix, dist)
corrected_frame_width = corrected_frame.shape[1]
corrected_frame_height = corrected_frame.shape[0]

out = cv2.VideoWriter(output_file, fourcc, fps, (corrected_frame_width, corrected_frame_height))

print(f"Recording video to {output_file}")

# Measure the start time for recording
recording_start_time = time.time()

while True:
    ret, frame = vcap.read()
    if not ret:
        print("Error: Unable to read frame from video stream")
        break
    
    corrected_frame = undistort_image(frame, cameraMatrix, dist)
    
    # Write the frame to the output file
    out.write(corrected_frame)
    
    # Check if 15 seconds have passed
    if time.time() - recording_start_time >= 15:
        print("Recording complete: 15 seconds elapsed")
        break

# Measure the end time for recording
recording_end_time = time.time()

record_time = recording_end_time - recording_start_time

print(f"Recorded for {record_time:.2f} seconds")


# Release the video capture and writer objects
vcap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video recording stopped. Saved to {output_file}")
