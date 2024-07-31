import time
import os
import sys
import termios
import tty
import threading
import json
import serial
import serial.tools.list_ports

import cv2
import numpy as np

from pymycobot.mycobot import MyCobot


# all of the code before the definition of the Arm class only exists as set up and is a compy from Threshold.py

port: str
mc: MyCobot
sp: int = 80


def setup():
    print("")
    global port, mc
    plist = list(serial.tools.list_ports.comports())
    idx = 1 
    port = "/dev/ttyAMA0"
    print(port)
    print("")
    baud = 1000000
    DEBUG = False
    mc = MyCobot(port, baud, debug=DEBUG)


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
        self.recording = False
        self.playing = False
        self.record_list = []
        self.record_t = None
        self.play_t = None
        self.rotationspeed = 40

    # sets the gripper to open
    def gripper_opened(self):
        self.mc.set_gripper_value(45,self.rotationspeed)
        print("Der Greifer wurde geöffnet.")

    # sets the gripper to close
    def gripper_closed(self):
        self.mc.set_gripper_value(8,self.rotationspeed)
        print("Der Greifer wurde geschlossen.")

    def set_to_take_out_position(self):
        self.mc.set_encoders([3222, 2712, 1590, 1975, 2361, 1373], self.rotationspeed)
        time.sleep(3)
        self.mc.set_encoders([3223, 2970, 1587, 1818, 2406, 3509], self.rotationspeed)
        time.sleep(0.5)
        print("Der Roboterarm ist in Entnahmeposition.")

    # sets cobot to home position
    def home(self):
        self.mc.set_encoders([986, 2072, 1023, 1999, 1933, 598], 30)
        print("Der Roboterarm fährt auf die Homeposition.")
    
    # lets the cobot freeze in position    
    def stop(self):
        self.mc.stop() 
        print("Der Roboterarm hält die Position.")

    # lets the cobot relax ! make shure it doesn't hit anything !    
    def release_servos(self):
        self.mc.release_all_servos()
        print("Der Roboterarm ist frei beweglich.")


    def rotate_gripper(self, rotation):
        self.mc.set_encoders([1576, 1024, 2043, 2007, 11, 1634], self.rotationspeed)
        time.sleep(3)
        angles = self.mc.get_angles()
        starting_angle = angles[5]
        self.mc.set_gripper_value(8, self.rotationspeed)
        time.sleep(0.5)
        while rotation > 45:
            angles[5] = starting_angle + 45
            self.mc.send_angles(angles, self.rotationspeed)
            print(angles)
            time.sleep(0.5)
            self.mc.set_gripper_value(45, self.rotationspeed)
            time.sleep(0.5)
            self.home()
            time.sleep(3)
            angles[5] = 0
            self.mc.send_angles(angles, self.rotationspeed)
            print(angles)
            time.sleep(0.5)
            self.mc.set_gripper_value(8, self.rotationspeed)
            rotation = rotation-45
            time.sleep(0.5)
        if rotation <= 45:
            angles[5] = rotation
            self.mc.send_angles(angles, self.rotationspeed)
            time.sleep(0.5)
            self.mc.set_gripper_value(45,self.rotationspeed)
    




    # teach in
    def record(self, ti_filename):
        self.record_list = []
        self.recording = True
        self.mc.set_fresh_mode(0)
        self.mc.release_all_servos()

        # starting the teach in
        print("Teach-In gerstartet...")

        def _record():
            start_t = time.time()

            while self.recording:
                angles = self.mc.get_encoders()
                if angles:
                    self.record_list.append(angles)
                    with open(ti_filename, "w") as json_file:
                        json.dump(self.record_list, json_file)
                    time.sleep(0.1)
                    print("\r {}".format(time.time() - start_t), end="")

        self.record_t = threading.Thread(target=_record, daemon=True)
        self.record_t.start()

    # stops writing the data stream for the teach in
    def stop_record(self):
        print("\nTeach-In gestoppt.")
        self.recording = False
        self.record_t.join()

    # cobots follows the teach in coordinate data stream, can also be run in the reversed order
    def play(self, ti_filename, backwards=False):
        print("\nTeach-In-Daten werden abgespielt.")
        time.sleep(0.1)
        with open(ti_filename) as jsonfile:
            self.record_list = json.load(jsonfile)
        if backwards:
            recorded = list(reversed(self.record_list))
        else: recorded = self.record_list
        for angles in recorded:
            self.mc.set_encoders(angles, 44)
            time.sleep(0.1)
        print("Teach-In-Daten fertig abgespielt.")
        time.sleep(1.0)

    def take_out_of_centrifuge(self):
        print("Entladen von Position 10.")
        self.set_to_take_out_position()
        time.sleep(3)
        self.gripper_closed()
        filename = "TakeOut.json"
        time.sleep(0.5)
        self.play(ti_filename = filename)
        self.home()


    # all manual uses are accessed by a keybind
    def manual_input(self, filename):
        while True:
            with Raw(sys.stdin):
                key = sys.stdin.read(1)
                if key == "b":
                    break # in case one wants to stop the program
                elif key == "o":
                    self.gripper_opened()
                elif key == "c":
                    self.gripper_closed()
                elif key == "h":
                    self.home()
                elif key == "e":
                    self.set_to_take_out_position()
                elif key == "f":
                    self.release_servos()
                elif key == "s":
                    self.stop()
                elif key == "r":
                    self.rotate_gripper(rotation = 160)
                elif key == "x":
                    coordinates = self.mc.get_coords
                    print(coordinates) # shows you x, y, z coordinates
                elif key == "a":
                    angles = self.mc.get_angles()
                    print(angles) # shows you the angles of all joints
                elif key == "g":
                    pos = self.mc.get_encoders()
                    print(pos)
                elif key == "t":
                    if self.recording:
                        self.stop_record()
                    else:
                        self.record(ti_filename = filename)
                elif key == "p":
                    self.play(ti_filename = filename)
                elif key == "q":
                    self.play(ti_filename = filename, backwards = True)
                elif key == "z":
                    self.take_out_of_centrifuge()
                else:
                    print(key)
                    continue


if __name__ == "__main__":
    setup()
    print("Please input the file name you want to edit.")
    teach_in_filename = "TakeOut.json"
    arm = Arm(mc)
    arm.home()
    arm.manual_input(teach_in_filename) # starts checking for manual input
