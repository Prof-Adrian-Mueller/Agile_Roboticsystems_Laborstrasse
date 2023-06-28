#!/usr/bin/env python

import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType
from time import sleep


"""-------The DoBot Control Class-------
Variables:
suction = Suction is currently on/off
picking: shows if the dobot is currently picking or dropping an item
api = variable for accessing the dobot .dll functions
home% = home position for %
                                  """

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}

#Main control class for the DoBot Magician.
class DoBotArm:
    def __init__(self, homeX, homeY, homeZ):
        self.suction = False
        self.picking = False
        self.api = dType.load()
        self.homeX = homeX
        self.homeY = homeY
        self.homeZ = homeZ
        self.connected = False
        self.dobotConnect()

    def __del__(self):
        self.dobotDisconnect()

    #Attempts to connect to the dobot
    def dobotConnect(self):
        if(self.connected):
            print("You're already connected")
        else:
            state = dType.ConnectDobot(self.api, "", 115200)[0]
            if(state == dType.DobotConnect.DobotConnect_NoError):
                print("Connect status:",CON_STR[state])
                dType.SetQueuedCmdClear(self.api)

                dType.SetHOMEParams(self.api, self.homeX, self.homeY, self.homeZ, 0, isQueued = 1)
                dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
                dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)

                dType.SetHOMECmd(self.api, temp = 0, isQueued = 1)
                self.connected = True
                return self.connected
            else:
                print("Unable to connect")
                print("Connect status:",CON_STR[state])
                return self.connected

    #Returns to home location and then disconnects
    def dobotDisconnect(self):
        self.moveHome()
        if(self.suction):
            lastIndex = dType.SetEndEffectorSuctionCup( self.api, False, False, isQueued = 0)[0]
            self.suction = False
        dType.DisconnectDobot(self.api)

    #Delays commands
    def commandDelay(self, lastIndex):
        dType.SetQueuedCmdStartExec(self.api)
        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(200)
        dType.SetQueuedCmdStopExec(self.api)

    #Toggles suction peripheral on/off
    def toggleSuction(self):
        lastIndex = 0
        if(self.suction):
            lastIndex = dType.SetEndEffectorSuctionCup( self.api, False, False, isQueued = 0)[0]
            self.suction = False
        else:
            lastIndex = dType.SetEndEffectorSuctionCup(self.api, True, True, isQueued = 0)[0]
            self.suction = True
        sleep(0.25)
        self.commandDelay(lastIndex)
        

    #Moves arm to X/Y/Z Location
    def moveArmXYZ(self,x,y,z):
        lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, 0)[0]
        self.commandDelay(lastIndex)

    #Returns to home location
    def moveHome(self):
        lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, self.homeX, self.homeY, self.homeZ, 0)[0]
        self.commandDelay(lastIndex)

    #Toggles between hover and item level
    def pickToggle(self, itemHeight):
        lastIndex = 0
        positions = dType.GetPose(self.api)
        if(self.picking):
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, positions[0], positions[1], self.homeZ, 0)[0]
            self.picking = False
        else:
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, positions[0], positions[1], itemHeight, 0)[0]
            self.picking = True
        self.commandDelay(lastIndex)

    #Move with 10% to XYZ
    def moveSnailXYZ(self,x,y,z):
        dType.SetPTPCommonParams(self.api, 10, 10, isQueued = 1)
        lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, 0)[0]
        self.commandDelay(lastIndex)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)

    #Move with 10% to XYZ
    def moveSnailXYZR(self,x,y,z,r):
        dType.SetPTPCommonParams(self.api, 10, 10, isQueued = 1)
        lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r)[0]
        self.commandDelay(lastIndex)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)

    #Move with 10% to XYZ
    def moveInARCMode(self,pointA,pointB):
        dType.SetPTPCommonParams(self.api, 0.5, 0.5, isQueued = 1)
        dType.SetARCParams(self.api, 0.1, 0.1, 0.1, 0.1, isQueued = 1)
        lastIndex = dType.SetARCCmd(self.api, pointA, pointB, 0)[0]
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)
        self.commandDelay(lastIndex)

    def forceStop(self):
        dType.SetQueuedCmdForceStopExec(self.api)
        dType.SetQueuedCmdClear(self.api)
        dType.SetQueuedCmdStartExec(self.api)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)