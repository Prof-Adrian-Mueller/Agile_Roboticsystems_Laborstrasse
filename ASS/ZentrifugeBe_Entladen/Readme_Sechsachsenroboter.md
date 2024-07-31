In Cobot.py finden Sie die wichtigsten Funktionen die im Ramen der Agile Robotics Challange SomSem 2024 für den Cobot Elephant zur Entnahme eines Tubes mit dem Suction Cup geschrieben wurden.

Unload_Centrifuge_Suction_Pump.py ist ein Template zum Import und zur Ausführung des Codes. 

Unload_Centrifuge_Gripper.py ist der Code des vorhergegangenen Sprints zur Entnahme der Zentrifuge mit einem Gripper. Da es sich hierbei um Legacy-Code handelt ist dieses Script nicht auskommentiert.

Unload_Centrifuge_Suction_Pump.py und Cobot.py sollten im gleichen Verzeichnis liegen. Unload_Centrifuge_Gripper.py funktioniert als Stand Alone.


Imports und Set Up:

Alle Imports und das gesamte Set Up des Sechsachsenroboters liegt auf seinem Raspberry Pi. Dieser Code dient lediglich zur Referenz falls der Raspberry Pi des Roboters zerstört oder dessen Speicher formatiert werden sollte und um einen Überblick über die implementierten Funktionen zu bieten. 

Für den Code essentiell sind insbesondere die Installation der Packages 
pymycobot https://pypi.org/project/pymycobot/ und
RPi.GPIO https://pypi.org/project/RPi.GPIO/ (zur Ansteuerung der Suction Pump)

Die Python Version war 3.8.



Manuelle Bedienung:

Insbesondere zum Testen und für das Teach-In ist eine Manuelle Bedienung mit Key-Bindings erforderlich. Wenn Sie Unload_Centrifuge_Suction_Pump.py starten wird ihnen eine Liste an möglichen Key-Bindings angezeigt. Zudem lassen sich die einzelnen Servos über die Zahlentasten ansteuern. Die Ansteuerung läuft symmetrisch von innen nach außen:
1 5. Servo, positive Drehrichtung
2 4. Servo, positive Drehrichtung
3 3. Servo, positive Drehrichtung
4 2. Servo, positive Drehrichtung
5 1. Servo, positive Drehrichtung
6 1. Servo, negative Drehrichtung
7 2. Servo, negative Drehrichtung
8 3. Servo, negative Drehrichtung
9 4. Servo, negative Drehrichtung
0 5. Servo, negative Drehrichtung





Das Template für ein Script in dem Funktionen aus Cobot.py übernommen werden sollen sieht wie folgt aus:
import Cobot as c
from pymycobot.mycobot import MyCobot

port: str
mc: MyCobot
sp: int = 80


def setup():
    global port, mc
    port = "/dev/ttyAMA0"
    baud = 1000000
    DEBUG = False
    mc = MyCobot(port, baud, debug=DEBUG)


if __name__ == '__main__':
    setup()
    arm = c.Arm(mc)
    teach_in_file = "YourTeachInFileName.json"

YourTeachInFileName bitte mit dem Namen ihres (zu generierenden) Teach-In-Json-Files versehen. 




Funktionen in Cobot.py:
Alle wichtigen Funktionen fallen unter die Klasse Arm.


set_sucker(mode)
Die Suction Pump wird angesteuert.

mode = True um die Suction Pump an zu schalten
mode = False um die Suction Pump aus zu schalten
default: mode = False


stop() 
Der Roboterarm hält die Servos auf der Position auf der sie sich befinden fest. Dies ist von Bedeutung wenn beispielsweise eine bestimmte Position ausgegeben werden soll.


release_servos() 
Der Roboterarm lässt alle Servos los. Dies wird für das Manuelle Handling benötigt.
Achtung! Den Arm festhalten oder auf eine sichere Position bringen damit er nicht gegen etwas knallt!


record(ti_filename)
Startet das schreiben der Positionen (Winkel der Servos in Grad) in das unter ti_filename referenzierte Teach-In-File im Abstand von 0.05s (änderbar unter der Variable ti_speed).


stop_record()
Hält das schreiben der Positionen an.


play(ti_filename, rotationspeed, backwards)
Spielt die unter ti_filename gespeicherten Positionen ab.

rotationspeed() = Geschwindigkeit der Servos
default = 40 (von 1 bis 100)
backwards = Ob die Reihenfolge der Positionen umgekehrt werden soll. (True oder False)
default = False


get_position(output)
Gibt die Position des Sechsachsenroboters aus.
output = In welcher form die Position ausgegeben werden soll.
"a" oder "angles" für Winkel in Grad
"r", "rad" oder "radians" für Winkel in Rad
"c", "coords" oder "coordinates" für Eulersche Koordinaten
beliebig für die Encoder Values
default = "angles"


set_position(values, rotationspeed, move_type, value_type)
Lässt den Sechsachsenroboter an entsprechende Position fahren.

values = Liste der Positionsangaben in der Form von value_type (analog zu output in get_position) an die der Sechsachsenroboter fahren soll
rotationspeed = Geschwindigkeit der Servos
default = 40
move_type:
0, "movej" oder "moveJ" = Der Sechsachsenroboter Springt von Position zu Position
beliebig = Direkte Bewegung von Position zu Position
default = 1


home() Setzt den Roboterarm auf die Homepostion ([-84.28, -0.79, 0.52, -156.09, 75.84, 78.39], Winkel in Grad, Sprungbewegung).


manual_input(filename):
Erwartet die Eingabe von Key-Bindings in der Konsole und gibt eine Liste der möglichen Keys aus. (Siehe Manuelle Bedienung)

