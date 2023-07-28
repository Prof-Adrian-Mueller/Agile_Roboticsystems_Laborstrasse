# Agile_Roboticsystems_Laborstrasse
Repository für die automatische Laborstraße des Agile Roboticsystems Projekt

Das System besteht aus 3 Teilprojekten:

- Die autmatische Laborstraße
- Das automatische Entladen
- Das automatische Tracking

## Einrichtung

Python 3.9 installieren\
Neustes Java installieren\
Befehl "pip -r Tracker_Config/requirements.txt" zum installieren der notwendigen Module im Terminal im Root Projektordner ausführen.\


## Automatische Laborstraße

Wird über die main.py in dem Ordner Main ausgeführt.\
Die Steuerung wird durch die doBot_Steuerung.py realisiert.\

Die Projekte Entladen und Tracking sind mit eingebunden\

## Automatisches Entladen

Befindet sich indem Ordner Entladen\

## Tracking

Eine genaue Dokumentation findet man unter Dokumentation_Tracker.pdf\

Das Tracking besteht aus 2 Teilen.\
Dem Erkennen der Micro-QR-Codes. Dieser befindet sich in dem Ordner Erkennen.\
Und dem Tracker, der in dem Monitoring Ordner liegt.\

Die Micro-Qr-Code Erkennung wird über die microqr_reader.py ausgeführt.\
Wurde diese importiert, kann über die Methode microqr_reader() die Erkennung gestartet werden.\
Der notwendige Parameter ist die Anzahl an Tubes, die erkannt werden wollen.\
Die Erkennung läuft solange, bis die angegebene Anzahl an Tubes erkannt wurde\
Es wird eine Liste zurückgegeben, die die Ids der erkannten Tubes, sowie deren Mittelpunktkoordinate enthält  [(xy,id)]\
Weitere Informationen bitte der Dokumentation entnehmen.\

Der Tracker wird über die monitoring.py ausgeführt.\
Wurde diese importiert, kann über die start_tracking() der Tracker gestartet werden.\
Der notwendige Paramteter ist der Rückgabewert der Micor-Qr-Code Erkennung\
Der Tracker läuft parallel zu Laborstraße, bis es manuell beendet wird.\
Die Ergebnisse werden in dem in der Tracker_Config/tracker_config.ini angegebenen Zielordner utner dem aktuellen Datum und Uhrzeit als .csv Datei gespeichert.\
Weitere Informationen bitte der Dokumentation entnehmen.\


