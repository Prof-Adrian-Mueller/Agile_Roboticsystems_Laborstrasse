from DobotEDU import *

import numpy as np
from PIL import Image


# Kreiert ein Foto
image_array = util.get_image(timeout=1, port=1, flip=False)
print(image_array[0][0][0])
bgr = []

# Wandelt rgb in bgr
for i in range(0, len(image_array)):
    for j in range(0, len(image_array[0])):
        r = image_array[i][j][0]
        g = image_array[i][j][1]
        b = image_array[i][j][2]
    entry = [b, g, r]
    bgr.append(entry)
bgr = np.array(bgr)

# Kreiert und zeigt das Bild
image = Image.fromarray(bgr)
image.show()
