# Micro-QR-Code Reader
Dieses Programm basiert grundlegend auf der Entwicklung von _Mirko Mettendorf_ im Rahmen des Projektes _Agile Roboticsystem Laborstraße_ .
Link zum Repository (Modul Erkennen und Monitoring):
https://github.com/Prof-Adrian-Mueller/Agile_Roboticsystems_Laborstrasse

## Voraussetzungen
Die benötigten Bibliotheken für Python 3.9 sind der Datei _requirements.txt_ zu entnehmen.
Es muss eine funktionierende USB-Verbindung zu einer Kamera vorhanden sein, um das Programm in seiner Standardversion nutzen zu können.
Weiteres kann der Dokumentation _Dokumentation_Tracking_Prototyp_Laborstraße.pdf_ entnommen werden.

## Verwendung
1. repository downloaden
2. [wenn nötig] Python 3.9 installieren
3. [wenn nötig] Bibliotheken installieren
	--> pip install -r requirements.txt
4. [optional] Kamera auswählen
	--> in main.py camtype in der Hauptfunktion auf:
	-	CamType.Standard: Hautpwebcam wird verwendet
	-	CamType.TopDown: Deckenkamera (IP-Cam) wird verwendet
		**WICHTIG**: IP muss ausgelesen und in der Datei _tracker_config.ini_ hinterlegt werden (mehr dazu, auch in der erwähnten Doku)
5. main.py ausführen

[optional] Bei Verwendung von Anker Kameras kann die Software _AnkerWork_ verwendet werden. 
Hier können Parameter wie Kontrast, Helligkeit, Schärfe, Auflösung sowie auch Einstellungen betreffend dem Autofokus angepasst werden.

--> Hauptfenster öffnet sich in voller Auflösung (2560x1440) \
--> mittels der Regler, lassen sich Kontrast und Belichtung anpassen \
--> erkannte Micro-QR-Codes werden rot umrahmt und die aufgelöste Information angezeigt
