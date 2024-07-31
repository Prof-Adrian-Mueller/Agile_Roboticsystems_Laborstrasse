from DobotEDU import *

import numpy as np


# Position als Punkt in xyz-Koordinaten
def get_position():
    position = m_lite.get_pose()
    x = position["x"]
    y = position["y"]
    z = position["z"]
    position = [x, y, z]
    return position


# Berechnet die Position der Tubes anhand eines Punktes
def calculate_positions(start, x_step, y_step):
    points = []
    for i in range(0, 4):
        points.append([])
        for j in range(0, 8):
            new_position = [start[0] + j * x_step, start[1] + i * y_step, start[2]]
            points[i].append(new_position)
    points = np.array(points)
    return points


if __name__ == '__main__':
    print("Setze den Roboterkopf auf ein Röhrchen in der rechten oberen Ecke des zu bestückenden Halters.")
    print("Drücke danach eine beliebige Taste um fortzufahren.")
    input()
    new_starting_point = get_position()
    print("Setze den Roboterkopf auf ein Röhrchen in der rechten oberen Ecke des bestückten Halters.")
    print("Drücke danach eine beliebige Taste um fortzufahren.")
    input()
    starting_point = get_position()
    # starting_point = [1, 1, 0]
    # new_starting_point = [-12, -12, 0]
    x_distance = 8 + 11.56/2
    y_distance = 5.66 + 11.56/2

    # Positionen Entnahme und Beladen
    positions = calculate_positions(starting_point, x_distance, y_distance)
    move_to = calculate_positions(new_starting_point, x_distance, x_distance)

    # Ein Array das festlegt welche Punkte im Rack angefahren werden/belegt sind
    occupied = np.zeros((4, 8))
    occupied[0, 2] = 1
    occupied[1, 3] = 1
    print(occupied)

    # Vorgang Entnahme und Beladen
    for a in range(0, 3):
        for b in range(0, 7):
            if occupied[a, b] == 1:
                x, y, z = positions[a, b]
                new_x, new_y, new_z = move_to[a, b]
                m_lite.set_ptpcmd(ptp_mode=0, x=x, y=y, z=z, r=0)
                m_lite.wait(1)
                m_lite.set_endeffector_suctioncup(enable=True, on=True)
                m_lite.wait(1)
                m_lite.set_ptpcmd(ptp_mode=0, x=new_x, y=new_y, z=new_z, r=0)
                m_lite.wait(1)
                m_lite.set_endeffector_suctioncup(enable=False, on=False)
                m_lite.wait(1)
                print([x, y, z])
                print([new_x, new_y, new_z])
            else:
                pass
    m_lite.set_homecmd()
