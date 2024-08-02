import json
import re
import time
from typing import Dict

import pandas as pd

from DBService.DBUIAdapter import DBUIAdapter
from GUI import Utils
from GUI.Model.LiveTubeStatus import LiveTubeStatus, FinalTubeStatus
from GUI.Storage.BorgSingleton import TubeLayoutSingleton, MainWindowSingleton, CurrentExperimentSingleton, \
    LiveDataResult, ExperimentSingleton
from GUI.Storage.Cache import Cache
from GUI.Utils.CheckUtils import CheckUtils, load_cache
from GUI.Utils.LiveObservable import LiveObserver


class LiveViewMessageDisplay(LiveObserver):
    def __init__(self):

        self.live_data = {}
        self.final_results = LiveDataResult()
        self.ui_db = DBUIAdapter()

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
        elif 'MONITORING_COMPLETED' in message:
            print("validating ...")
            self.validate_end_result()
        else:
            # Unrecognized message format
            print("Unrecognized message format.")
        # print(f"Received message LiveViewMessageDisplay: {tube_status}")

    def save_result_in_db(self, final_result):
        main_singleton = MainWindowSingleton()

        current_exp_id = CurrentExperimentSingleton()
        self.update_final_result(final_result)
        self.final_results.add_data(final_result.tube_id, final_result)
        # probe_nr, Startstation, Startzeit, Zielstation, Zielzeit, Dauer, Zeitstempel
        self.ui_db.insert_tracking_log(current_exp_id.experiment_id, final_result.tube_id, final_result.start_station,
                                       final_result.start_station_time, final_result.end_station,
                                       final_result.end_station_time, final_result.duration,
                                       final_result.video_timestamp)

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

    def update_final_result(self, final_result):
        tube_layout = TubeLayoutSingleton()
        tube_layout.add_station_details(final_result.tube_id, final_result)

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
            start_station_time = str(data.get('startStationTime', ''))
            end_station = str(data.get('endStation', ''))
            end_station_time = str(data.get('endStationTime', ''))
            duration = float(data.get('duration', 0.0))
            video_timestamp = float(data.get('videoTimestamp', 0.0))

            return FinalTubeStatus(tube_id, start_station, start_station_time, end_station, end_station_time, duration,
                                   video_timestamp)
        except ValueError as e:
            # Handle data conversion errors or invalid data here
            raise ValueError(f"Error processing data: {str(e)}")

    def validate_end_result(self):
        try:
            print("validate_end_result")

            # Assuming CurrentExperimentSingleton provides current experiment ID in some manner
            current_exp = CurrentExperimentSingleton()
            experiment_id = current_exp.experiment_id if current_exp.experiment_id else \
            load_cache(Cache("application_cache.json"))["experiment_id"]

            if experiment_id:
                tubes = self.ui_db.get_tubes_by_exp_id(experiment_id)
                if tubes:
                    print("tubes")
                    print(tubes)

                for tube in tubes:
                    tube_id = tube['probe_nr']
                    if self.final_results.get_data(str(tube_id)):
                        print(f"{tube_id}: Success")
                    else:
                        print(f"{tube_id}: Failed")
                        tube_layout = TubeLayoutSingleton()
                        buttons = tube_layout.get_button_layout(tube_id)
                        if buttons:
                            color = "#FF0000"
                            buttons[0].setStyleSheet(f"QPushButton {{ background-color: {color}; }}")
                            buttons[1].setStyleSheet(f"QPushButton {{ background-color: {color}; }}")
                            buttons[2].setStyleSheet(f"QPushButton {{ background-color: {color}; }}")
                            final_tube_status = FinalTubeStatus(tube_id, None, None, None, None, None, None)
                            self.update_final_result(final_tube_status)

        except Exception as ex:
            print(ex)
        #         self.update_button_color(result_status, "#FF0000")  # Red for failure or incomplete
        #     else:
        #         self.update_button_color(result_status, "#4CAF50")  # Green for success
        # # for tube_id, result_status in self.final_results.get_all_data():
        #     live_status = self.final_results.get_data(tube_id)
        #     if live_status and not live_status.left_station and result_status.end_station != "End":
        #         self.update_button_color(result_status, "#FF0000")  # Red for failure or incomplete
        #     else:
        #         self.update_button_color(result_status, "#4CAF50")  # Green for success
