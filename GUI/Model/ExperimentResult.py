from datetime import datetime


class ExperimentResult:
    def __init__(self, id, experiment, tube_nr, start_station, start_time, end_station, end_time, duration,
                 video_timestamp):
        self.id = id
        self.experiment = experiment
        self.tube_nr = tube_nr
        self.start_station = start_station
        self.start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        self.end_station = end_station
        self.end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        self.duration = duration
        self.video_timestamp = float(video_timestamp)

    def __repr__(self):
        return f"<ExperimentResult id={self.id} experiment={self.experiment}>"

    @staticmethod
    def map_data_to_model(data_tuples):
        results = []
        for data in data_tuples:
            result = ExperimentResult(*data)
            results.append(result)
        return results
