import time
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
    teach_in_file = "Test.json"
    arm.manual_input(teach_in_file)
    
