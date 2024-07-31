from DobotEDU import *

import json


# Aktuelle Position
position = m_lite.get_pose()

# Versucht ein TeachIn.json zum Editieren zu öffnen und fügt die aktuelle Position hinzu.
# Existiert TeachIn.json nicht, so wird das Json-File kreiert.
try:
    with open('TeachIn.json', 'r') as file:
        positions = json.load(file)
        positions.extend([position])
except FileNotFoundError:
    positions = position
with open('TeachIn.json', 'w') as file:
    json.dump(positions, file)
