import json
import re
from typing import Dict

import pandas as pd

from GUI.Model.LiveTubeStatus import LiveTubeStatus, FinalTubeStatus
from GUI.Storage.BorgSingleton import TubeLayoutSingleton
from GUI.Utils.LiveObservable import LiveObserver


class LiveViewMessageDisplay(LiveObserver):
    def __init__(self):
        self.live_data = {}
        self.final_results = {}

    def notify(self, message):
        global tube_status
        if 'nextStationDistance' in message:
            # This is a LiveTubeStatus message
            tube_status = self.parse_live_message(message)
            self.live_data[tube_status.tube_id] = tube_status
            self.update_button_color(tube_status, "#4CAF50")
        elif 'startStationTime' in message or 'videoTimestamp' in message:
            data_dict = {}
            for line in message.strip().split('\n'):
                key, value = line.split(None, 1)
                key = key.strip()
                value = value.strip()
                data_dict[key] = value

            try:
                tube_status = self.parse_final_message(data_dict)
                self.save_result_in_db(tube_status)
            except ValueError as e:
                # Handle parsing or processing errors
                print(f"Error processing data: {str(e)}")
        else:
            # Unrecognized message format
            print("Unrecognized message format.")
        print(f"Received message LiveViewMessageDisplay: {tube_status}")

    def save_result_in_db(self, final_result):
        print("TODO Save in DB " + str(final_result))

    def update_button_color(self, tube_status, color):
        tube_layout = TubeLayoutSingleton()
        buttons = tube_layout.get_button_layout(tube_status.tube_id)
        if buttons:
            station_index_mapping = {"Start": 0, "Thymio": 1, "Deckelentnahme": 2}
            if tube_status.last_station in station_index_mapping:
                button_index = station_index_mapping[tube_status.last_station]
                buttons[button_index].setStyleSheet(f"QPushButton {{ background-color: {color}; }}")
                tube_layout._shared_state['station_info'].setdefault(str(tube_status.tube_id), [None, None, None])
                tube_layout._shared_state['station_info'][str(tube_status.tube_id)][button_index] = {
                    "name": f"Station {button_index}", "details": f"{tube_status}"}

    @staticmethod
    def parse_live_message(message):
        # Split the message into lines and ignore the last line
        lines = message.strip().split('\n')[:-1]  # Discard 'Name: 0, dtype: object'

        # Parse each line to extract the key and value
        data = {}
        for line in lines:
            key, value = line.split(maxsplit=1)
            key = key.strip()
            value = value.strip()
            data[key] = value

        # Convert to the appropriate data types
        tube_id = int(data.get('tubeID', 0))
        last_station = data.get('lastStation', '')
        left_station = data.get('leftStation', 'False') == 'True'
        next_station = data.get('nextStation', '')
        next_station_distance = None if data.get('nextStationDistance', 'NaN') == 'NaN' else float(
            data['nextStationDistance'])

        return LiveTubeStatus(tube_id, last_station, left_station, next_station, next_station_distance)

    @staticmethod
    def parse_final_message(data: Dict[str, str]) -> FinalTubeStatus:
        if not isinstance(data, dict):
            raise ValueError("Input data is not a dictionary.")

        try:
            tube_id = str(data.get('tubeID', ''))
            start_station = str(data.get('startStation', ''))
            start_station_time = pd.to_datetime(data.get('startStationTime', ''))
            end_station = str(data.get('endStation', ''))
            end_station_time = pd.to_datetime(data.get('endStationTime', ''))
            duration = float(data.get('duration', 0.0))
            video_timestamp = float(data.get('videoTimestamp', 0.0))

            return FinalTubeStatus(tube_id, start_station, start_station_time, end_station, end_station_time, duration,
                                   video_timestamp)
        except ValueError as e:
            # Handle data conversion errors or invalid data here
            raise ValueError(f"Error processing data: {str(e)}")

    def validate_end_result(self):
        for tube_id, result_status in self.final_results.items():
            live_status = self.live_data.get(tube_id)
            if live_status and not live_status.left_station and result_status.end_station != "End":
                self.update_button_color(result_status, "#FF0000")  # Red for failure or incomplete
            else:
                self.update_button_color(result_status, "#4CAF50")  # Green for success
