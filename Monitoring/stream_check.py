import cv2

def check_rtsp_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Could not open stream.")
        return False

    ret, frame = cap.read()
    if ret:
        print("Stream is active. Frame captured successfully.")
        # Optionally, display the frame using cv2.imshow("Frame", frame) and wait for a key press.
        # Ensure you're running this in an environment where you can display images.
        return True
    else:
        print("Stream is active, but could not capture a frame.")
        return False

    cap.release()

rtsp_url = 'rtsp://admin:admin@192.168.137.173:554/11'
check_rtsp_stream(rtsp_url)
