import time
from dobot.DobotDllType import DobotDllType as dType


api = dType.load()

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

state = dType.ConnectDobot(api, "", 115200)[0]

if state == dType.DobotConnect.DobotConnect_NoError:
    print("Connect status:", CON_STR[state])
else:
    print("Connect status:", CON_STR[state])
    exit()

# Clear previous commands
dType.SetQueuedCmdClear(api)

# Set the Dobot to coordinate mode
dType.SetHOMEParams(api, 200, 0, 20, 0, isQueued=1)
dType.SetHOMECmd(api, temp=0, isQueued=1)
dType.SetQueuedCmdStartExec(api)
time.sleep(2)  # wait for homing to complete

# X axis
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 0, 20, 0, isQueued=1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 0, 20, 0, isQueued=1)

# Y axis
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 100, 20, 0, isQueued=1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, -100, 20, 0, isQueued=1)

# Z axis
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 0, 50, 0, isQueued=1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 0, 10, 0, isQueued=1)

# sliding rail
dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 0, 20, 0, 100, isQueued=1)
dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 0, 20, 0, 0, isQueued=1)

# Activate GPIO pin
dType.SetIODO(api, dType.IODO.DO17, 1, isQueued=1)
time.sleep(1) 
dType.SetIODO(api, dType.IODO.DO17, 0, isQueued=1)

# Wait for commands to finish
dType.SetQueuedCmdStopExec(api)
dType.DisconnectDobot(api)
