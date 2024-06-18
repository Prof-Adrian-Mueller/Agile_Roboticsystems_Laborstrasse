"""Micro Qr Reader, erkennt alle Micro-QR-Codes aus dem Video und prüft die Anzahl"""

__author__ = 'Mirko Mettendorf'
__date__ = '20/05/2023'
__version__ = '1.0'
__last_changed__ = '13/07/2023'

import datetime
import time
from configparser import ConfigParser

import cv2
import numpy as np

from Tracker_Config.path_configuration import PathConfiguration
from Tracker_Config.tracker_utils import VideoCapture, berechne_mittelpunkt, send_to_telegram

import pyboof as pb



# Lese Config Datei
# config_object = ConfigParser()
# config_object.read("..\\Tracker_Config\\tracker_config.ini")
path_config = PathConfiguration()
config_object = path_config.load_configuration()
cameraConf = config_object["Camera"]
telegramConf = config_object["Telegram"]
trackerConf = config_object["Tracker"]


from enum import Enum
class CamType(Enum):
    TopDown = f'rtsp://admin:admin@{cameraConf["cameraIp"]}:554/11'
    Standard = 0



# Lese Tracking Config Werte aus
MAX_QR_WAIT_TIME = int(trackerConf["wait_qr_time"])

# MicroQRCode Config
config = pb.ConfigMicroQrCode()
config.version = 1
config.maxIterations = 10
config.maximumSizeFraction = 0.8
config.minimumSizeFraction = 0.01


def microqr_reader(count):
    """ Startet den MicroQrReader und versucht alle MicroQrCodes im Video zu erkennen.

    Args:
        count (int): Die zu erkennende Anzahl an Tubes

    Returns:
        tuple: Ein Tupel (count,tube_ids) bei dem count die Anzahl an erkannten tubes und tube_ids eine Liste mit den
        Tube_IDs und den Koordinaten der Bounding Box ist
    """
    print("QR Reader gestartet")
    # TODO : send this status to GUI , QR Button green in Live View

    # Bereite Kamera vor
    cap = cv2.VideoCapture(0)
    cv2.waitKey(1)

    # Erzeuge QRReader Objekt
    factory = pb.FactoryFiducial(np.uint8)
    detector = factory.microqr(config=config)

    # Erzeuge Fenster
    cv2.namedWindow('Erkannte Marker', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Erkannte Marker', cv2.WND_PROP_TOPMOST, 1)
    # cv2.resizeWindow('Erkannte Marker', 1920, 1080)

    # Berechne Kameramatrix mit Kalibrierdaten/ für ubs webcam eigentlich nicht notwendig
    # bei Bedarf Kalibrierung dieser erst durchführen
    #mtx, dist = calibrate_Camera.load_coefficients('calibration_charuco.yml')
    #newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (3840, 2160), 0, (1920, 1080))
    #mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (1920, 1080), 5)

    # Stoppe Zeit
    start_time = datetime.datetime.now()

    # für jeden Frame
    while True:

        # vergangene Zeit
        past_time = datetime.datetime.now() - start_time

        # lese Frame
        flag, img = cap.read()

        # überspringen, wenn kein frame vorhanden
        if img is None:
            break

        # Entzerre Kamera (optional)
        #dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        #x, y, w, h = roi
        #dst = dst[y:y + h, x:x + w]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = pb.ndarray_to_boof(gray)

        # Bildkopie
        output_image = img.copy()

        # erkenne QR-Codes
        detector.detect(image)

        # Liste mit den IDs und Koordinaten der QR-Codes
        tube_ids = []

        # für jede Erkennung
        for qr in detector.detections:
            print("message: '" + qr.message + "'")
            # TODO QR Message in Live View

            # speicher Koordinaten
            points = np.array([tuple(c) for c in qr.bounds.convert_tuple()], dtype=np.int32)

            # erzeuge Bounding-box
            cv2.rectangle(output_image, points[3], points[1], (0, 0, 255), 3)
            cv2.putText(output_image, qr.message, (points[1][0], points[1][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 0, 255), 2)

            # berechne Mittelpunkt
            xy = berechne_mittelpunkt(points[3], points[1])

            # füge Tupel in Liste hinzu
            tube_ids.append((xy, int(qr.message)))

        # Zeige Video an
        cv2.imshow('Erkannte Marker', output_image)

        # notwendig, damit Frame angezeigt werden kann
        cv2.waitKey(1)

        # Tube Anzahl ist korrekt, gibt Anzahl und Liste zurück
        if len(detector.detections) >= count:
            print("Richtige Anzahl an Tubes erkannt")
            cap.release()
            #cv2.destroyAllWindows()
            print(tube_ids)
            # TODO Green GUI, everything ok to read QR
            return tube_ids

        # Tube Anzahl ist falsch, nach Ablauf der Zeit Warnung herausschicken und nach 30 Sekunden wiederholen
        else:
            print("Nicht korrekte Anzahl an Tubes erkannt")
            if past_time.seconds > MAX_QR_WAIT_TIME:
                send_to_telegram("Es wurden nicht alle Tubes in der vorgegebenen Zeit erkannt. Bitte überprüfen")
                time.sleep(30)
                start_time = datetime.datetime.now()
                # TODO Red GUI, everything not ok to read QR

    # beende auslesen der Kamera
    cap.release()
    # TODO Wissam - die Anfangszeit & Endezeit  für Tracking; anzahl tubes, status : ok?
    # beende alle Fenster
    cv2.destroyAllWindows()


#microqr_reader(4)

def microqr_reader_show_detection(camtype=CamType.Standard):
    print("QR Reader gestartet")
    # TODO : send this status to GUI , QR Button green in Live View

    # Bereite Kamera vor
    cap = cv2.VideoCapture(camtype.value)
    cv2.waitKey(1)

    # Erzeuge QRReader Objekt
    factory = pb.FactoryFiducial(np.uint8)
    detector = factory.microqr(config=config)

    # Erzeuge Fenster
    cv2.namedWindow('Erkannte Marker', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Erkannte Marker', cv2.WND_PROP_TOPMOST, 1)
    # cv2.resizeWindow('Erkannte Marker', 1920, 1080)
    cv2.createTrackbar('V1 min', 'Erkannte Marker', 0, 255, nothing)
    cv2.createTrackbar('V1 max', 'Erkannte Marker', 255, 255, nothing)
    cv2.createTrackbar('V2 min', 'Erkannte Marker', 0, 255, nothing)
    cv2.createTrackbar('V2 max', 'Erkannte Marker', 255, 255, nothing)
    cv2.createTrackbar('V3 min', 'Erkannte Marker', 0, 255, nothing)
    cv2.createTrackbar('V3 max', 'Erkannte Marker', 255, 255, nothing)


    # Berechne Kameramatrix mit Kalibrierdaten/ für ubs webcam eigentlich nicht notwendig
    # bei Bedarf Kalibrierung dieser erst durchführen
    #mtx, dist = calibrate_Camera.load_coefficients('calibration_charuco.yml')
    #newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (3840, 2160), 0, (1920, 1080))
    #mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (1920, 1080), 5)

    # Stoppe Zeit
    start_time = datetime.datetime.now()

    # für jeden Frame
    while True:

        # vergangene Zeit
        past_time = datetime.datetime.now() - start_time

        # lese Frame
        flag, img = cap.read()

        # überspringen, wenn kein frame vorhanden
        if img is None:
            break

        v1min = cv2.getTrackbarPos('V1 min', 'Erkannte Marker')
        v1max = cv2.getTrackbarPos('V1 max', 'Erkannte Marker')
        v2min = cv2.getTrackbarPos('V2 min', 'Erkannte Marker')
        v2max = cv2.getTrackbarPos('V2 max', 'Erkannte Marker')
        v3min = cv2.getTrackbarPos('V3 min', 'Erkannte Marker')
        v3max = cv2.getTrackbarPos('V3 max', 'Erkannte Marker')

        lower = np.array([v1min, v2min, v3min], dtype=np.uint8)
        upper = np.array([v1max, v2max, v3max], dtype=np.uint8)

        temp = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        threshold_img = cv2.inRange(img, lower, upper)

        result_frame = cv2.bitwise_and(img, img, mask=threshold_img)
        cv2.imshow('Threshold', result_frame)


        # Entzerre Kamera (optional)
        #dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        #x, y, w, h = roi
        #dst = dst[y:y + h, x:x + w]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = pb.ndarray_to_boof(gray)

        # Bildkopie
        output_image = img.copy()

        # erkenne QR-Codes
        detector.detect(image)

        # Liste mit den IDs und Koordinaten der QR-Codes
        tube_ids = []

        # für jede Erkennung
        for qr in detector.detections:
            # TODO QR Message in Live View

            # speicher Koordinaten
            points = np.array([tuple(c) for c in qr.bounds.convert_tuple()], dtype=np.int32)

            # erzeuge Bounding-box
            cv2.rectangle(output_image, points[3], points[1], (0, 0, 255), 3)
            cv2.putText(output_image, qr.message, (points[1][0], points[1][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 1)

            # berechne Mittelpunkt
            xy = berechne_mittelpunkt(points[3], points[1])

            # füge Tupel in Liste hinzu
            tube_ids.append((xy, int(qr.message)))

        # Zeige Video an
        cv2.imshow('Erkannte Marker', output_image)

        # notwendig, damit Frame angezeigt werden kann
        key = cv2.waitKey(1)

        if key == 27 or key == ord('c') or key == ord('C'):
            break

    # beende auslesen der Kamera
    cap.release()
    # TODO Wissam - die Anfangszeit & Endezeit  für Tracking; anzahl tubes, status : ok?
    # beende alle Fenster
    cv2.destroyAllWindows()

def microqr_reader_show_detection_contrast(camtype=CamType.Standard):
    print("QR Reader gestartet")
    # TODO : send this status to GUI , QR Button green in Live View

    # Bereite Kamera vor
    cap = cv2.VideoCapture(camtype.value, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
    cv2.waitKey(1)

    # Erzeuge QRReader Objekt
    factory = pb.FactoryFiducial(np.uint8)
    detector = factory.microqr(config=config)

    # Erzeuge Fenster
    cv2.namedWindow('Erkannte Marker', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Erkannte Marker', cv2.WND_PROP_TOPMOST, 1)
    #cv2.resizeWindow('Erkannte Marker', 1920, 1080)
    cv2.createTrackbar('contrast', 'Erkannte Marker', 0, 255, nothing)
    cv2.createTrackbar('brightness', 'Erkannte Marker', 255, 255, nothing)

    # Berechne Kameramatrix mit Kalibrierdaten/ für ubs webcam eigentlich nicht notwendig
    # bei Bedarf Kalibrierung dieser erst durchführen
    #mtx, dist = calibrate_Camera.load_coefficients('calibration_charuco.yml')
    #newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (3840, 2160), 0, (1920, 1080))
    #mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (1920, 1080), 5)

    # Stoppe Zeit
    start_time = datetime.datetime.now()

    # für jeden Frame
    while True:

        # vergangene Zeit
        past_time = datetime.datetime.now() - start_time

        # lese Frame
        flag, img = cap.read()
        #print(f"height {img.shape[0]}    width {img.shape[1]}")

        # überspringen, wenn kein frame vorhanden
        if img is None:
            break

        contrast = cv2.getTrackbarPos('contrast', 'Erkannte Marker')
        brightness = cv2.getTrackbarPos('brightness', 'Erkannte Marker')

        adjusted_img = cv2.addWeighted(img, 1 + contrast / 127.0, img, 0, brightness - 255)

        #result_frame = cv2.bitwise_and(img, img, mask=threshold_img)
        #cv2.imshow('test', adjusted_img)


        # Entzerre Kamera (optional)
        #dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        #x, y, w, h = roi
        #dst = dst[y:y + h, x:x + w]
        gray = cv2.cvtColor(adjusted_img, cv2.COLOR_BGR2GRAY)
        image = pb.ndarray_to_boof(gray)
        #cv2.imshow("test", gray)

        # Bildkopie
        output_image = adjusted_img.copy()

        # erkenne QR-Codes
        detector.detect(image)

        # Liste mit den IDs und Koordinaten der QR-Codes
        tube_ids = []

        # für jede Erkennung
        for qr in detector.detections:
            # TODO QR Message in Live View

            # speicher Koordinaten
            points = np.array([tuple(c) for c in qr.bounds.convert_tuple()], dtype=np.int32)

            # erzeuge Bounding-box
            cv2.rectangle(output_image, points[3], points[1], (0, 0, 255), 3)
            cv2.putText(output_image, qr.message, (points[1][0], points[1][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)

            # berechne Mittelpunkt
            xy = berechne_mittelpunkt(points[3], points[1])

            # füge Tupel in Liste hinzu
            tube_ids.append((xy, int(qr.message)))

        # Zeige Video an
        cv2.imshow('Erkannte Marker', output_image)

        # notwendig, damit Frame angezeigt werden kann
        key = cv2.waitKey(1)

        if key == 27 or key == ord('c') or key == ord('C'):
            break

    # beende auslesen der Kamera
    cap.release()
    # TODO Wissam - die Anfangszeit & Endezeit  für Tracking; anzahl tubes, status : ok?
    # beende alle Fenster
    cv2.destroyAllWindows()

def nothing(val):
    None
