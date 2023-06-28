# Created by Dimitri Papyschew
# Auflösung ist 640x480, für die Kallibrierung Tube and der Entnahmeposition x=320 and y=240 positionieren
# Verwenden Sie zum Kallibrieren calibration.py

import DoBotArm as Dbt
import threading
import cv2
import numpy as np
import argparse
# zu test Zwecken
from time import sleep


#@@@@@@@@@@@@@@@@@
#GLOBALE PARAMETER
#@@@@@@@@@@@@@@@@@

#!!!!!!WICHTIG!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Falls Anwahl des Programms nicht von der SHELL aus gestartet wird ARGUMENT nrTubes auskommentieren!!!!!!!!!!!!!!!!!!

parser = argparse.ArgumentParser()
parser.add_argument("-nr", "--number", help="Number of Tubes")
args = parser.parse_args()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

found = False
#Minimaler und Maximaler Radius der zu suchenden Durchmesser
minRad = 18
maxRad = 20

#Treshhold wie viele mm sind in x,y für Entnahme verkraftbar
#Je größer desto ungenauer der Haltepunkt, dafür aber sicherer die Erkennung
tolaranceMiddlePoint =  0.5

#Initialisierung Dobot mit HomePos 250,0,50
homeX, homeY, homeZ = 250, 0, 50
ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ) #Create DoBot Class Object with home position x,y,z

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#Funktion zum drehen der Zentrifuge
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#Funktion zum drehen der Zentrifuge
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def movePlate():

    #Punkte Auf der Drehplatte bei 0, 45 und 90 Grad
    #Falls Dobot versetzt wurde bitte aktualisieren
    point1 = [260.6, -3.1, -100]
    point2 = [271.6, 24.2, -100, -45]
    point3 = [304, 38.6, -100,-45]

    global ctrlBot
    while True:
        ctrlBot.moveArmXYZ(point1[0], point1[1], point1[2]+20)
        ctrlBot.moveSnailXYZ(point1[0], point1[1], point1[2])
        ctrlBot.moveInARCMode(point2,point3)
       
        if found:
            ctrlBot.forceStop()
            break
        
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#Funktion zum entladen der Zentrifuge
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def unload(tubeNr):
    global ctrlBot
    firstReleasePos = [0, 0, 0]
    #_ ROw _____________________________
    #|posN      .....  p8   p4
    #|posN-1    .....  p7   p3= [fristPosX +- 0 * deltaX], [fristPosY +- 2 * deltaY], [fristPosZ +- 0* deltaZ]
    #|posN-2    .....  p6   p2= [fristPosX +- (tubeNR /  numberOfTubesperColumn) * deltaX], [fristPosY +- (tubeNR mod numberOfTubesPerRow) * deltaY], [fristPosZ +- (tubeNR / numberOfTubesPerRow) * deltaZ]
    #|PosN-3    .....  p5   p1= firstPos
    #-------------------------------
    deltaX,deltaY,deltaZ = 10, 10, 10
    numberOfTubesPerRow = 5

    currentX = firstReleasePos[0] + (int)(tubeNr/ numberOfTubesPerRow) *deltaX
    currentY = firstReleasePos[1] + np.divmod(tubeNr, numberOfTubesPerRow)[1] *deltaY
    currentZ = firstReleasePos[2] + (int)(tubeNr/ numberOfTubesPerRow) *deltaZ

    #Entladeposition Tubes
    #Falls Dobot versetzt wurde bitte aktualisieren
    unloadPosition = [275.6, 0, -91.6]
    print(f"{tubeNr}, {currentX}, {currentY}, {currentZ}")

    ctrlBot.moveHome()
    ctrlBot.moveArmXYZ(unloadPosition[0],unloadPosition[1],unloadPosition[2]+20)
    ctrlBot.moveSnailXYZ(unloadPosition[0],unloadPosition[1],unloadPosition[2])
    ctrlBot.toggleSuction()
    ctrlBot.moveArmXYZ(unloadPosition[0],unloadPosition[1],unloadPosition[2]+20)
    ctrlBot.moveHome()
    ctrlBot.toggleSuction()
    ctrlBot.moveArmXYZ(currentX,currentY,currentZ)
    

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#Funktion zur Erkennung der Tube Positionen
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def searchForTubes():
    global found
    cap = cv2.VideoCapture(0)
    detected_circles = None

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while detected_circles is None or found is False:
        # aufnahme Frame für Frame
        ret, frame = cap.read()
        # wenn frame richtig gelesen wurde gehe weiter sonst...
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Frame wird in Graustufen umgewandelt
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Dimesionen der einzeilnen Bilder kann anstatt 320,240 verwendet werden falls die Kameraauflösund sich ändert
        # height, width = np.uint16(np.around(frame.shape[:2]))

        # Verschwimmen der Bilder mit 3 * 3 kernel um Rauschen zu entfernen.
        gray_blurred = cv2.GaussianBlur(gray, (3, 3),0)

        # Sucht nach Kreisen mit dem Hough Gradianten 
        # HoughCircles(Image,method,dp,minDist,param1,param2,minRadius,maxRadius)
        # image:	    8-bit, single-channel, grayscale input image.
        # circles:	    output vector of found circles(cv.CV_32FC3 type). Each vector is encoded as a 3-element floating-point vector (x,y,radius) .
        # method:	    detection method(see cv.HoughModes). Currently, the only implemented method is HOUGH_GRADIENT
        # dp:	        inverse ratio of the accumulator resolution to the image resolution. For example, if dp = 1 , the accumulator has the same resolution as the input image. If dp = 2 , the accumulator has half as big width and height.
        # minDist:	    minimum distance between the centers of the detected circles. If the parameter is too small, multiple neighbor circles may be falsely detected in addition to a true one. If it is too large, some circles may be missed.
        # param1:	    first method-specific parameter. In case of HOUGH_GRADIENT , it is the higher threshold of the two passed to the Canny edge detector (the lower one is twice smaller).
        # param2:	    second method-specific parameter. In case of HOUGH_GRADIENT , it is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first.
        # minRadius:	minimum circle radius.
        # maxRadius:	maximum circle radius.

        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 30, param1 = 50, param2 = 50, minRadius = minRad, maxRadius = maxRad)

        if detected_circles is not None:
             for x in detected_circles[0,:]:
                a, b, r = x[0], x[1], x[2]

                # Falls x +- Toleranze und y +- Toleranze passt -> Tube an Entnahmeposition gefunden -> Entnahme
                if(np.isclose(b,240,atol = tolaranceMiddlePoint) and np.isclose(a,320,atol = tolaranceMiddlePoint)):
                    print("CENTRE FOUND STOP TURNING!")
                    found = True 
                    break
                # Falls x +- Toleranze und y +- Toleranze passt -> Print -> Tube nährt sich der Entnahmeposition
                if(np.isclose(b,240,atol = 3*tolaranceMiddlePoint) and np.isclose(a,320,atol = 3*tolaranceMiddlePoint)):
                    print(a,b)
    # Bilderaufnahme beenden
    cap.release()
    cv2.destroyAllWindows 

#Hauptfunktion mit Übergabeparameter Anzahl der Tubes
def main(nrTubes):
    global found
    print(f"ENTLADE {nrTubes}!")
    for x in range(nrTubes):
        # Asynchrones abarbeiten der Methoden
        t1 = threading.Thread(target=movePlate)
        t2 = threading.Thread(target=searchForTubes)
        t1.start()
        t2.start()
        # Haltevoraussetzung Tube wurde gefunden found = True
        t2.join()
        ctrlBot.forceStop()
        
        unload(x,nrTubes)
        found = False
        print(f"iterration endet, Tube {x} of, {nrTubes} Unloadet")

if __name__ == "__main__":
    main(args.number)