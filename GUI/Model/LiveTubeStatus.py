class LiveTubeStatus:
    def __init__(self, tube_id, last_station, left_station, next_station, next_station_distance):
        self.tube_id = tube_id
        self.last_station = last_station
        self.left_station = left_station
        self.next_station = next_station
        self.next_station_distance = next_station_distance

    def __repr__(self):
        return str({
            "tube_id": self.tube_id,
            "last_station": self.last_station,
            "left_station": self.left_station,
            "next_station": self.next_station,
            "next_station_distance": self.next_station_distance
        })


class FinalTubeStatus:
    def __init__(self, tube_id, start_station, start_station_time, end_station, end_station_time, duration, video_timestamp):
        self.tube_id = tube_id
        self.start_station = start_station
        self.start_station_time = start_station_time
        self.end_station = end_station
        self.end_station_time = end_station_time
        self.duration = duration
        self.video_timestamp = video_timestamp

    def __repr__(self):
        return str({
            "tube_id": self.tube_id,
            "start_station": self.start_station,
            "start_station_time": self.start_station_time,
            "end_station": self.end_station,
            "end_station_time": self.end_station_time,
            "duration": self.duration,
            "video_timestamp": self.video_timestamp
        })

    def __iter__(self):
        # Example: yield each attribute value
        yield self.tube_id
        yield self.start_station
        yield self.start_station_time
        yield self.end_station
        yield self.end_station_time
        yield self.duration
        yield self.video_timestamp

    def to_dict(self):
        # Convert the object's attributes to a dictionary
        return {
            'tube_id': self.tube_id,
            'start_station': self.start_station,
            'start_station_time': self.start_station_time,
            'end_station': self.end_station,
            'end_station_time': self.end_station_time,
            'duration': self.duration,
            'video_timestamp': self.video_timestamp,
        }