import pandas as pd


class StationMonitor:
    def __init__(self, log_path, log_detail_path):
        self.log_df = pd.read_csv(log_path)
        self.log_detail_df = pd.read_csv(log_detail_path)
        self.stations = ['Start', 'Thymio', 'Deckelentnahme']

    def print_station_info(self):
        print("Station Information for Each Frame (log_detail.csv):")
        for index, row in self.log_detail_df.iterrows():
            tube_id = row['tubeID']
            last_station = row['lastStation']
            left_station = "Yes" if row['leftStation'] else "No"
            next_station = row['nextStation']
            print(f"Tube {tube_id} - Last Station: {last_station}, Left Station: {left_station}, Next Station: {next_station}")

    def print_end_result(self):
        print("\nEnd Result for Each Tube (log.csv):")
        for station in self.stations:
            print(f"\n--- Station: {station} ---")
            station_logs = self.log_df[self.log_df['startStation'] == station]
            for index, row in station_logs.iterrows():
                tube_id = row['tubeID']
                if row['endStation'] == station:
                    status = "GREEN LIGHT"
                else:
                    status = "RED LIGHT"
                print(f"Tube {tube_id} at {station}: {status}")


# Maximum allowed duration at each station (example values)
max_duration = {'Thymio': 30, 'Deckelentnahme': 45}  # Duration in seconds or appropriate units

# Initialize the StationMonitor with the provided CSV files
station_monitor = StationMonitor('../SimulationData/case_1/log.csv', '../SimulationData/case_1/log_detail.csv')

# Simulate the station monitoring
print("Starting Station Monitoring Simulation...")
station_monitor.print_station_info()
station_monitor.print_end_result()
