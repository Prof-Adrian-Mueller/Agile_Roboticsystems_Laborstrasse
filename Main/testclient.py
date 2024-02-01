import cv2

from Monitoring.monitoring import cameraConf

# Specify the filename of the input and output videos
input_filename = 'C:\\Users\\Fujitsu\\Documents\\video.mkv'
output_filename = 'output_video.mp4'

# Open the input video
cap = cv2.VideoCapture(input_filename)
# RTSP_URL = 'rtsp://admin:admin@' + cameraConf["cameraIp"] + ':554/11'
# cap = cv2.VideoCapture(RTSP_URL)

# Check if the video was opened successfully
if not cap.isOpened():
    print(f"Error: Could not open video {input_filename}")
    exit()

# Get the video frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object using H264 codec
fourcc = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame_width, frame_height))

# Read and write the video frame by frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Write the frame to the output video
    out.write(frame)

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()

print("Video processing complete.")
