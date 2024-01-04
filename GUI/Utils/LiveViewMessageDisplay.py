from GUI.Model.LiveTubeStatus import LiveTubeStatus
from GUI.Storage.BorgSingleton import TubeLayoutSingleton
from GUI.Utils.LiveObservable import LiveObserver


class LiveViewMessageDisplay(LiveObserver):
    def notify(self, message):
        tube_status = self.parse_message(message)
        print(f"Received message LiveViewMessageDisplay: {tube_status}")
        buttons = TubeLayoutSingleton().get_button_layout(tube_status.tube_id)
        if buttons and tube_status.next_station == "Thymio":
            # Change the color of the first button to blue
            buttons[0].setStyleSheet("QPushButton { background-color: #4CAF50; }")

        # Check if the second station (next_station) is "Deckelentnahme"
        if buttons and getattr(tube_status, 'next_station', None) == "Deckelentnahme":
            # Change the color of the second button to green
            buttons[1].setStyleSheet("background-color: #4CAF50;")

    @staticmethod
    def parse_message(message):
        # Split the message into lines and ignore the last line
        lines = message.strip().split('\n')[:-1]  # Discard 'Name: 0, dtype: object'

        # Parse each line to extract the key and value
        data = {}
        for line in lines:
            # Split the line on the longest whitespace sequence
            key, value = line.split(maxsplit=1)
            # Remove any additional whitespace around the key and value
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
