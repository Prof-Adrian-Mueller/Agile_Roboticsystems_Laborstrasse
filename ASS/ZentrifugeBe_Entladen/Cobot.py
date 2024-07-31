import sys
import time
import termios
import tty
import threading
import json
import RPi.GPIO as GPIO  # Import for Sucker Pump
from pymycobot.mycobot import MyCobot 


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)  # GPIO Port is 7

ti_speed = 0.05
menu_text = ("Drücke...\n"
             "b um das Programm zu stoppen.\n"
             "h um auf die Homeposition zu fahren.\n"
             "o um die Suction Pump an/aus zu schalten.\n"
             "t um das Teach In zu starten/stoppen.\n"
             "p um das Teach In abzuspielen.\n"
             "q um das Teach In umgekehrt abzuspielen.\n"
             "f um alle Servos zu entspannen.\n"
             "s um alle Servos festzuhalten.\n"
             "g um die Servo-Größen zu erhalten.\n"
             "a um die Servo-Winkel in Grad zu erhalten.\n"
             "r um die Servo-Winkel in Rad zu erhalten.\n"
             "x um die Eulerschen Koordinaten des letzten Servos zu erhalten.")
            

class Raw(object):
    """Set raw input mode for device"""

    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)
        
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)


class Arm(object):
    def __init__(self, mycobot) -> None:
        super().__init__()
        self.mc = mycobot
        self.sucking = False
        self.recording = False
        self.playing = False
        self.record_list = []
        self.record_t = None
        self.play_t = None
        self.ti_speed = ti_speed
        self.speed = 60

    def set_sucker(self, mode=False):
        if mode:
            GPIO.output(7, GPIO.LOW)  # LOW to turn the suction pump on
        else:
            GPIO.output(7, GPIO.HIGH)  # HIGH to turn the suction pump off

    # dadurch lässt sich der Roboter genau Positionieren
    def stop(self):
        self.mc.stop() 
        print("\nDer Roboterarm hält die Position.")

    # Wird zur manuellen Bewegung des Roboterarmes benötigt
    def release_servos(self):
        self.mc.release_all_servos()
        print("\nDer Roboterarm ist frei beweglich.")

    # Teach In Stream
    def record(self, ti_filename):
        self.record_list = []
        self.recording = True
        self.mc.set_fresh_mode(0)
        self.mc.release_all_servos()
        print("\nTeach-In gerstartet...")

        def _record():
            start_t = time.time()

            while self.recording:
                angles = self.mc.get_angles()
                if angles:
                    self.record_list.append(angles)
                    with open(ti_filename, "w") as json_file:
                        json.dump(self.record_list, json_file)
                    time.sleep(self.ti_speed)
                    print("\r {}".format(time.time() - start_t), end="")

        self.record_t = threading.Thread(target=_record, daemon=True)
        self.record_t.start()

    # Stoppt das Schreiben der Teach In Datei
    def stop_record(self):
        print("\nTeach-In gestoppt.")
        self.recording = False
        self.record_t.join()

    # cobots follows the teach in coordinate data stream, can also be run in the reversed order
    def play(self, ti_filename, rotationspeed=40, backwards=False):
        print("\nTeach-In-Daten werden abgespielt.")
        time.sleep(0.1)
        try:
            with open(ti_filename) as jsonfile:
                self.record_list = json.load(jsonfile)
            if backwards:
                recorded = list(reversed(self.record_list))
            else:
                recorded = self.record_list
            for values in recorded:
                self.mc.send_angles(values, rotationspeed)
                time.sleep(0.1)
            print("\nTeach-In-Daten fertig abgespielt.")
            time.sleep(1.0)
        except FileNotFoundError:
            print('Kein Teach-In-Daten gefunden.')

    # Gibt Informationen über die Servostellungen des Roboters, dessen Positionierung zurück
    def get_position(self, output="angles"):
        if output == "a" or "angles":
            angles = self.mc.get_angles()
            return angles
        elif output == "r" or "rad" or "radians":
            rad = self.mc.get_radians()
            return rad
        elif output == "c" or "coords" or "coordinates":
            coords = self.mc.get_coords()
            return coords 
        else:
            pos = self.mc.get_encoders()
            return pos
            
    # Bewegt den Roboter        
    def set_position(self, values, rotationspeed=40, move_type=1, value_type="angles"):
        if move_type == 0 or "movej" or "moveJ":
            move_type = 0
        else: 
            move_type = 1
        self.mc.set_movement_type(move_type)

        if value_type == "a" or "angles":
            self.mc.send_angles(values, rotationspeed)
        elif value_type == "r" or "rad" or "radians":
            self.mc.send_radians(values, rotationspeed)
        elif value_type == "c" or "coords" or "coordinates":
            self.mc.send_coords(values, rotationspeed) 
        else:
            self.mc.set_encoders(values, rotationspeed)

    # Die Homeposition ist in der Regel gut erreichbar und der Roboter steht selbst im entspannten Zustand stabiel
    def home(self):
        self.set_position([-84.28, -0.79, 0.52, -156.09, 75.84, 78.39], move_type="movej")

    # Keybindings für die Obigen funktionen ermöglichen die Bedienung des Roboters
    def manual_input(self, filename):
        print(menu_text)

        while True:

            with Raw(sys.stdin):
                key = sys.stdin.read(1)
                if key == "b":
                    self.home()
                    self.release_servos()
                    self.set_sucker(mode=False)
                    break  # in case one wants to stop the program
                if key == "h":
                    self.home()

                elif key == "o":
                    if self.sucking:
                        self.set_sucker(mode=False)
                        self.sucking = False
                    else:
                        self.set_sucker(mode=True)
                        self.sucking = True

                elif key == "t":
                    if self.recording:
                        self.stop_record()
                    else:
                        self.record(ti_filename=filename)
                elif key == "p":
                    self.play(ti_filename=filename)
                elif key == "q":
                    self.play(ti_filename=filename, backwards=True)

                elif key == "f":
                    self.release_servos()
                elif key == "s":
                    self.stop()

                elif key == "g":
                    pos = self.get_position(output="g")
                    print(pos)
                elif key == "r":
                    pos = self.get_position(output="r")
                    print(pos)
                elif key == "a":
                    pos = self.get_position(output="a")
                    print(pos)
                elif key == "x":
                    pos = self.get_position(output="c")
                    print(pos)

                elif key == "1":
                    self.mc.jog_increment(5, 2, self.speed)
                elif key == "0":
                    self.mc.jog_increment(5, -2, self.speed)
                elif key == "2":
                    self.mc.jog_increment(4, 2, self.speed)
                elif key == "9":
                    self.mc.jog_increment(4, -2, self.speed)
                elif key == "3":
                    self.mc.jog_increment(3, 2, self.speed)
                elif key == "8":
                    self.mc.jog_increment(3, -2, self.speed)
                elif key == "4":
                    self.mc.jog_increment(2, 2, self.speed)
                elif key == "7":
                    self.mc.jog_increment(2, -2, self.speed)
                elif key == "5":
                    self.mc.jog_increment(1, 2, self.speed)
                elif key == "6":
                    self.mc.jog_increment(1, -2, self.speed)

                else:
                    print(key)
                    continue


# Dieses Script ist als Import gedacht: Siehe Unloading_Centrifuge.py für die Anwendung.
if __name__ == '__main__':
    pass
