# STEUERZENTRALE
# Autor: David Weyer
# Dokumentation: https://stax124.github.io/DobotAPI/
# Importiere DoBot API
import dobotapi

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
        invalid_input=False
        print("Eingabe: " + str(anzahl_tubes))

# Dobot initialisieren und einer Variable zuweisen
dobot = dobotapi.Dobot
# Verbindung aufbauen
dobot.ConnectDobot()
# Interface initialisieren
dobot.SetIOMultiplexing(14, 0, 1)  # Set the user interface I/O to an input

# Code von Papyshew wird aufgerufen
# Payshewfunction()
# Rückgabe wird abgeglichen -> evtl abbruch

# EventListener = wartet auf einen Input auf Pin 14 vom DoBot-Interface
while True:
    io_status = dobot.GetIODI(14)

    if io_status == 1:  # Wenn der Input ausgelöst wird
        print("Whisker-Input detected!")

        # Code von Mettendorf wird aufgerufen
        # Mettendorffunction()
        # Rückgabe wird abgeglichen -> evtl abbruch

        # Loop: Wiederhole die Tube Entnahme (i = anzahl_tubes)
        offset_x = 0
        offset_y = 0
        for i in range(anzahl_tubes):
            # DoBot fährt auf HOME-Position
            dobot.move_to(34.9336, -212.3015, 134.8012, -80.6559, MODE_PTP.MOVL_XYZ )
            # DoBot fährt auf Position des Tubes (Position des 1. Tubes + Offset)
            dobot.move_to(97.5212+offset_x, -221.1407+offset_y, 63.6053, -66.2029, MODE_PTP.MOVL_XYZ)
            # DoBot verrechnet offset -> geht 3 Reihen à 4 Tubes durch
            offset_x += 21.6
            if i == 3 or i == 7:
                offset_y += 19.25
                offset_x = 0
            # Lade .playback File
            playback_file = "./XOXOXOXO.playback"
            dobot.SetPlaybackCmd(playback_file)
            # Starte das Playback
            dobot.Playback()
            #
            # Abfrage: Wird das letzte Tube bearbeitet -> wenn ja, wird der Blocker am Ende bewegt
            if i == anzahl_tubes - 1:
                playback_file = "./MoveBlocker.playback"
                dobot.SetPlaybackCmd(playback_file)
                dobot.Playback()
    break

    # Verbindung trennen
    dobot.DisconnectDobot()

# Thymio fährt weiter...
#ENDE
