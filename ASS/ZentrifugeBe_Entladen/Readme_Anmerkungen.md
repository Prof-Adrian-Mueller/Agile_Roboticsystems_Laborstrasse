Die Dokumentation des Cobot Elephants und der damit zusammenhängenden Python API pymycobot ist stark fehlerbehaftet. Es hatte mich viel Zeit gekostet herauszufinden was wie funktioniert und was nicht. Im Folgenden finden Sie eine Zusammenfassung der Erfahrungen die ich bei der Arbeit mit dem Sechsachsenroboter gemacht habe:

Während die Dokumentation behauptet man könnte den Sechsachsenroboter mit Eulerkoordinaten ansteuern, so ist das fern von der Realität. Die Rotationskoordinaten scheinen lediglich die Rotationen der letzten drei Servo-Motoren zu sein. Für die Koordinaten interpoliert der Cobot Elephant am meisten, das Resultat sind in der Regel ungewollte Bewegungen und oft kommt der Sechsachsenroboter nicht dort zu stehen wo man vermuten würde. Daher kann ich das Nutzen von Koordinaten nicht empfehlen. Objekte im Raum können deshalb auch nicht über Koordinaten gekennzeichnet werden. Um Objekte zu vermeiden ist es besser eine Position an den Roboterarm zu senden die ihn in seiner Bewegung das Objekt vermeiden lässt.

Der Interpolation des Sechsachsenroboters ist generell nicht zu vertrauen. Die am besten nachvollziehbaren Bewegungen scheinen Angle-Values zu geben. Daher ist entweder die jog_increment()-Funktion oder eine hohe Dichte an Angle-Koordinaten die über send_angles() an die Servos gesendet werden, wie z.B. beim Teach-In, zu empfehlen. Die jog_increment()-Funktion nimmt tatsächlich Winkel in Grad und nicht Koordinaten wie in der API behauptet (der Rest dieser Funktionen funktioniert nicht richtig oder zumindest nicht wie beschrieben). 

Leider erlaubt die jog_increment()-Funktion nur die Rotation eines Servos zu einem Zeitpunkt. Schade, denn diese Bewegung ist die nachvollziehbarste des Sechsachsenroboters.
Die Manuelle Steuerung des Sechsachsenroboters wurde implementiert da das manuelle heben des Roboterarms die Position des Armes bei der Ausgabe verfälscht. Als Test um herauszufinden wie sich der Arm am zuverlässigsten bewegen lässt und um die Präzision der Bewegung zu erhöhen. Leider ist zweiteres durch die Einschränkung immer nur einen Servo zu bewegen sehr Eingeschränkt. Ich hatte eine Funktion geschrieben um dieses Problem zu lösen, konnte sie aus Zeitmangel allerdings nicht mehr debuggen.

Der Roboterarm besitzt Schutzmechanismen. Wenn gegen einen Servo ein zu großer Widerstand wirkt, so ist er nicht mehr ansteuerbar. Dreht sich ein Servo über sein virtuelles Limit (das etwas geringer ist als sein tatsächliches) so gibt er seine Servo-Stellungen oder Koordinaten als leere Liste aus. 

Die Sechs Servos des Roboterarmes scheinen unterschiedlich stark. Die Motoren nahe der Basis halten die Position besser als die vorderen Motoren. Das ist auch der Grund weshalb der Endeffektor des Roboters die Trommel der Zentrifuge nicht einfach in der Mitte angreifen und drehen kann. 
Ist der Roboterarm zu instabil und erreicht die gewünschte Position nicht, so schwenkt er die vorderen Glieder hin und her um die Position und Stabilität zu erreichen. Das ist problematisch, da der Raum in dem der Arm sich bewegt durch die Zentrifuge eingeschränkt ist.
Der Arm fängt nach langer Laufzeit teilweise an sich von selbst zu bewegen. Der Raspberry Pi wird nach langer Laufzeit sehr viel langsamer.

Kein wirkliches Problem, aber störend: Nach einem Neustart wechselt der Raspberry Pi immer auf das englische Keyboard Layout. 


Zu den Endeffektoren:

Die Suction Pump wird bei auf dem Wert 0 eingeschaltet und 1 ausgeschaltet.
Die GPIO-Anschlüsse werden entgegen dem Nutzerhandbuch wie folgt gesteckt: 
RPi.GPIO hatte sich aus irgend einem Grund auf der Pythonversion 3.8 installiert, weshalb wir die Version 3.11 vom Raspberry Pi entfernt haben.
Die Suction Pump muss mit dem Deckel des Tubes einen Formschluss bilden und ordentlich angedrückt werden um den Tube zu halten. Mit dem in wenigen Tagen selbst gebauten Sockel war eine Entsprechende Präzision nicht zu erreichen.

Der Gripper ist sehr breit weshalb er schnell an Teilen der Zentrifuge hängen bleibt und die Zentrifuge nicht voll bestückt werden kann. Der Roboterarm muss allerdings nicht so präzise sein wie beim Suction Cup, denn durch die breite der Kontaktflächen und die Weite in der sich der Gripper öffnet wird die Unschärfe in der Position ausgeglichen. Bevor ich den Roboterarm zu arg verschoben habe und eine Start-Endposition eingebaut hatte die verhindern sollte dass das Tube geschwenkt wird konnte ich in 20-30 Wiederholungen das Tube entnehmen.
