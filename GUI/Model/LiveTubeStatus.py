class LiveTubeStatus:
    def __init__(self, tube_id, last_station, left_station, next_station, next_station_distance):
        self.tube_id = tube_id
        self.last_station = last_station
        self.left_station = left_station
        self.next_station = next_station
        self.next_station_distance = next_station_distance

    def __repr__(self):
        return (f"LiveTubeStatus(tube_id={self.tube_id}, last_station='{self.last_station}', "
                f"left_station={self.left_station}, next_station='{self.next_station}', "
                f"next_station_distance={self.next_station_distance})")
