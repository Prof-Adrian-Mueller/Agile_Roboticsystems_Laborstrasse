import time
import DobotDllType as dType

# Load Dll
api = dType.load()

# Connect Dobot
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

state = dType.ConnectDobot(api, "", 115200)[0]

print("Connect status:", CON_STR[state])

if state == dType.DobotConnect.DobotConnect_NoError:
    # Set EIO port 13 to high
    # eio_port = 13
    # state = 1  # 1 for high, 0 for low
    # dType.SetIODO(api, eio_port, state)
    # print(f"port {eio_port} set to {state}")
    while True:
        
        # Read from EIO port 15
        eio_port = 13

        value = dType.GetIODI(api, eio_port)
        print(f"IODI value from port {eio_port}: {value}")
        value = dType.GetIOADC(api, eio_port)
        print(f"IOADC value from port {eio_port}: {value}")
        value = dType.GetIODIExt(api, eio_port)
        print(f"IODIEXT value from port {eio_port}: {value}")
        value = dType.GetIODO(api, eio_port)
        print(f"IODO value from port {eio_port}: {value}")
        value = dType.GetIODOExt(api, eio_port)
        print(f"IODOEXT value from port {eio_port}: {value}")
        value = dType.GetIOMultiplexing(api, eio_port)
        print(f"IOMult value from port {eio_port}: {value}")
        value = dType.GetIOMultiplexingExt(api, eio_port)
        print(f"IOMultExt value from port {eio_port}: {value}")

        time.sleep(1)

    # Disconnect Dobot
    dType.DisconnectDobot(api)
else:
    print("Failed to connect to Dobot")
