# STEUERZENTRALE
# Autor: David Weyer
# Dokumentation: https://stax124.github.io/DobotAPI/
# Importiere DoBot API
# Version 1.3
# Änderungen: python update mit requirements.txt
#             setplayback etc deaktiviert, nicht vorhanden
#             RTLD_Global gesetzt aber kein effekt; dlls nach main kopiert
#             Whisker detection funktioniert

# TODO: A: move_to zu offical api ändern,
#       B: while schleife und roboteransteurerung, und dissconnect
#       C: magnet funktionsfähig bekommen,
#       dieser code läuft im studio:
#       dType.SetIOMultiplexingEx(api, 17, 1, 1)
#       while True:
#           dType.dSleep(1000)
#           dType.SetIODO(api, 17, 1, isQueued=0)
#       D: klappt es beide apis zu benutzen ?
#       E: DLL Pfade aufräumen
import dobotapi as dobot

import Erkennen.microqr_reader as erkennen
import DobotDllType as dType


def steuerung():
    # Loop: Solange fragen bis man eine gültige Eingabe bekommt (Anzahl der Tubes abfragen)
    invalid_input = True
    while invalid_input:
        # Abfrage: Wieviele Tubes werden bearbeitet
        anzahl_tubes = int(input("Anzahl der Tubes eingeben: "))
        # Fehlerkennung: Eingabe muss eine Zahl zwischen 1 und 12 sein!
        if anzahl_tubes < 1 or anzahl_tubes > 12:
            print("Ungültige Eingabe -> Eingabe muss eine Zahl zwischen 1 und 12 sein!")
            continue
        # Ausgabe: Input
        else:
            invalid_input = False
            print("Eingabe: " + str(anzahl_tubes))

    # api laden
    api = dType.load()
    # Verbindung aufbauen
    state = dType.ConnectDobot(api, "", 115200)[0]
    # Interface initialisieren
    dType.SetIOMultiplexing(api, 14, 0, 1)  # Set the user interface I/O to an input

    # Code von Papyshew wird aufgerufen
    #entladen.main(anzahl_tubes)

    # EventListener = wartet auf einen Input auf Pin 14 vom DoBot-Interface
    while True:
        io_status = dType.GetIODI(api, 14) # Whisker called once due to break
        print(str(io_status))
        if io_status == [1]:  # Wenn der Input ausgelöst wird
            print("Whisker-Input detected!")
            #dType.SetIOMultiplexingEx(api, 17, 1,0) richtig aber bleibt hängen nur im studio
            #dType.SetIODO(api,17,1,0)
            #dType.dSleep(1000)
            print(str(dType.GetIODI(api,17)))
            # Code von Mettendorf wird aufgerufen
            erkennen.microqr_reader(anzahl_tubes)
            # Rückgabe wird abgeglichen -> evtl abbruch

            # Loop: Wiederhole die Tube Entnahme (i = anzahl_tubes)
            offset_x = 0
            offset_y = 0
            for i in range(anzahl_tubes):
                # DoBot fährt auf HOME-Position
                dobot.Dobot.move_to(34.9336, -212.3015, 134.8012, -80.6559,0,0.0) # grap from top with jump
                # DoBot fährt auf Position des Tubes (Position des 1. Tubes + Offset)
                dobot.move_to(97.5212 + offset_x, -221.1407 + offset_y, 63.6053, -66.2029,0,0.0)
                # DoBot verrechnet offset -> geht 3 Reihen à 4 Tubes durch
                offset_x += 21.6
                if i == 3 or i == 7:
                    offset_y += 19.25
                    offset_x = 0

                dobot.move_to()
                # Lade .playback File
                playback_file = "./XOXOXOXO.playback"
                dobot.SetPlaybackCmd(playback_file)
                # Starte das Playback
                dobot.Playback()
                #

                dType.SetIODO(api,17,1)
                # Abfrage: Wird das letzte Tube bearbeitet -> wenn ja, wird der Blocker am Ende bewegt
                #if i == anzahl_tubes - 1:
                    #playback_file = "./MoveBlocker.playback"
                    #dobot.SetPlaybackCmd(playback_file)
                    #dobot.Playback()


        # Verbindung trennen
        #dobot.DisconnectDobot()

    # Thymio fährt weiter...
    # ENDE
