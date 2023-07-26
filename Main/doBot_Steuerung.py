# STEUERZENTRALE
# Autor: David Weyer
# Version 1.6
# Änderungen: neue reqirements.txt für alle Projekte zusammen
#             DLL Ordner in Path Variable gesetzt, funkioniert nicht auf labor pc
#             Schleife funktioniert
#              magnet funktioniert
#             dobot fährt mit original api call und homing bei start


# TODO:
#       A: Ablauf für automatische Laborstraße
#       B: DLL aus Ordner zu laden funktioniert auf dem Laborpc nicht

import DLL.DobotDllType as dType
import Erkennen.microqr_reader as erkennen
#import Entladen.entladen as entladen



CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}





def steuerung():
    # api laden
    api = dType.load()
    # Verbindung aufbauen
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])
    if state == dType.DobotConnect.DobotConnect_NoError:
        dType.SetQueuedCmdClear(api)
        #Async Motion Params Setting
        dType.SetHOMEParams(api, 250, 0, 50, 200, isQueued = 1)
        dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

        #Async Home
        dType.SetHOMECmd(api, temp = 0, isQueued = 1)
        dType.dSleep(1000)
        # Loop: Solange fragen bis man eine gültige Eingabe bekommt (Anzahl der Tubes abfragen)
        invalid_input = True
        while invalid_input:
            # Abfrage: Wieviele Tubes werden bearbeitet
            print("Auf pipsen des Dobots warten")
            anzahl_tubes = int(input("Anzahl der Tubes eingeben: "))
            # Fehlerkennung: Eingabe muss eine Zahl zwischen 1 und 12 sein!
            if anzahl_tubes < 1 or anzahl_tubes > 12:
                print("Ungültige Eingabe -> Eingabe muss eine Zahl zwischen 1 und 12 sein!")
                continue
            # Ausgabe: Input
            else:
                invalid_input = False
                print("Eingabe: " + str(anzahl_tubes))





        # Code von Papyshew wird aufgerufen
        #entladen.main(anzahl_tubes)

        # EventListener = wartet auf einen Input auf Pin 14 vom DoBot-Interface
        while dType.GetIODI(api, 14)[0]!=1:
            print("wait for Whisker")


        # Wenn der Input ausgelöst wird
        print("Whisker-Input detected!")
        dType.SetIOMultiplexingEx(api, 17, 1, 0)
        dType.SetIODO(api,17,1,0)
        dType.dSleep(1000)
        dType.SetIODO(api, 17, 0, 0)
        print(str(dType.GetIODO(api,17)))
        # Code von Mettendorf wird aufgerufen
        #erkennen.microqr_reader(anzahl_tubes)
        # Rückgabe wird abgeglichen -> evtl abbruch

        # Loop: Wiederhole die Tube Entnahme (i = anzahl_tubes)
        offset_x = 0
        offset_y = 0
        for i in range(anzahl_tubes):
            # DoBot fährt auf HOME-Position
            dType.SetPTPCmd(api,dType.PTPMode.PTPJUMPXYZMode,34.9336, -212.3015, 134.8012, -80.6559) # grap from top with jump
            # DoBot fährt auf Position des Tubes (Position des 1. Tubes + Offset)
            dType.SetPTPCmd(api,dType.PTPMode.PTPJUMPXYZMode,97.5212 + offset_x, -221.1407 + offset_y, 63.6053, -66.2029)
            # DoBot verrechnet offset -> geht 3 Reihen à 4 Tubes durch
            offset_x += 21.6
            if i == 3 or i == 7:
                offset_y += 19.25
                offset_x = 0

            #TODO Bewegung Deckelabschrauben

            dType.SetIODO(api,17,1,0)
            # Abfrage: Wird das letzte Tube bearbeitet -> wenn ja, wird der Blocker am Ende bewegt
            #if i == anzahl_tubes - 1:
                #playback_file = "./MoveBlocker.playback"
                #dobot.SetPlaybackCmd(playback_file)
                #dobot.Playback()


        # Verbindung trennen
        dType.DisconnectDobot(api)

        # Thymio fährt weiter...
        # ENDE
