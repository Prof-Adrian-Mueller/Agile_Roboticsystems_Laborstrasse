"""Zum Starten des YOLOv8 Trainings"""

__author__ = 'Mirko Mettendorf'
__date__ = '20/05/2023'
__version__ = '1.0'
__last_changed__ = '13/07/2023'

from configparser import ConfigParser

from ultralytics import YOLO

# Lade das pretrained yolov8 Model
model = YOLO('yolov8n.pt')

# Lese Config Datei
config_object = ConfigParser()
config_object.read("tracker_config.ini")
yoloConf = config_object["Detektor"]

# Parameter
EPOCHS = int(yoloConf["epochs"])

# Trainiere das Model
if __name__ == '__main__':
    model.train(data='data.yaml', epochs=EPOCHS, imgsz=1280)