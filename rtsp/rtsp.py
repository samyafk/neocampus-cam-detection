import cv2

vcap = cv2.VideoCapture("rtsp://localhost:8554/profile2/media.smp")

while(1):

    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)

# # Define the RTSP URL
# rtsp_url = 'rtsp://localhost:8554/profile2/media.smp'

# # Create a VideoCapture object
# cap = cv2.VideoCapture(rtsp_url)

# # Check if the stream is opened successfully
# if not cap.isOpened():
#     print("Error: Could not open video stream")
#     exit()

# # Read and display the video stream frame by frame
# while True:
#     print("coucou")
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     if not ret:
#         print("Failed to grab frame")
#         break

#     # Display the resulting frame
#     cv2.imshow('RTSP Stream', frame)

#     # Break the loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything is done, release the capture
# cap.release()
# cv2.destroyAllWindows()