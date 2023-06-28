import cv2
import numpy as np

def main():
    tolaranceMiddlePoint = 0.5
    tolaranceRadius = 1
    minRad = 18
    maxRad = minRad+tolaranceRadius

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        gray_blurred = cv2.GaussianBlur(gray, (3, 3),0)

        cv2.imshow('Gray image', gray_blurred)

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 30, param1 = 50, param2 = 50, minRadius = minRad, maxRadius = maxRad)
        
        if detected_circles is not None:
            for x in detected_circles[0,:]:
                a, b, r = x[0], x[1], x[2]

                if(np.isclose(b,240,atol = tolaranceMiddlePoint) and np.isclose(a,320,atol = tolaranceMiddlePoint)):
                    print("CENTRE FOUND STOP TURNING!")
                    print(a,b)
                    break

                # Draw the circumference of the circle.
                # Convert the circle parameters a, b and r to integers.
                cv2.circle(frame, (np.uint16(np.around(a)), np.uint16(np.around(b))), np.uint16(np.around(r)), (0, 255, 0), 2)

                # Draw a small circle (of radius 1) to show the center.
                # Convert the circle parameters a, b and r to integers.
                cv2.circle(frame, (np.uint16(np.around(a)), np.uint16(np.around(b))), 1, (0, 0, 255), 1)  
                cv2.circle(frame, (320, 240), 1, (0, 0, 255), 1)
                cv2.circle(frame, (320, 240), 2, (0, 0, 255), 1)
                cv2.circle(frame, (320, 240), 3, (0, 0, 255), 1)
                # Display the resulting frame
                cv2.imshow('Found Cicles', frame)

        if cv2.waitKey(1) == ord('q'):
            break

main()

    

