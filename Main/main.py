import queue
import subprocess
import sys
import time
import threading

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '04/01/2024'

import cv2
import pandas as pd

from Monitoring.monitoring import Tube


class InterprocessCommunication:
    """
    Process to be run by GUI. Could Send and Receive Message to GUI.
    """

    def __init__(self, is_debug=False):
        self.is_debug = is_debug
        self.message_queue = queue.Queue()
        self.is_running = True

    def receive_message(self):
        while self.is_running:
            line = sys.stdin.readline().strip()
            if line:
                self.message_queue.put(line)
                if line == 'exit':
                    self.is_running = False


    def run_child_process(self):
        while self.is_running:
            try:
                # Check if there's a new message without blocking
                received_message = self.message_queue.get_nowait()
                print("E&T : " + received_message)
            except queue.Empty:
                pass  # No new message

    def live_simulation(self):
        file_path = "SimulationData\module_failed_sim\log_detail.csv"
        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            print("LIVE " + str(row))

        file_path = "SimulationData\case_1\log.csv"
        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            print("RESULT " + str(row))
            # time.sleep(2)
        strmsg = "Error_Test Tube " + str(1) + " ist seit " + str(
                            10) + " Sekunden in keiner Station aufgetaucht"
        print(f"ERROR_MESSAGE {strmsg}")
        tube_example = Tube(1, 101)
        print(f"ERROR_DATA {tube_example}")
        time.sleep(10)
        print("Simulation Complete!")
        print("MONITORING_COMPLETED")

    def run(self, args):
        anzahl_tubes = int(args[0])
        if self.is_debug:
            print("E&T Started! \n Type 'exit' to stop the process.")
        else:
            print("Starting steuerung")
            from Main.doBot_Steuerung import SteuerungControl
            steuerung = SteuerungControl(anzahl_tubes)
            steuerung.steuerung()

        self.start_listening_thread()

    def start_listening_thread(self):
        # Start the input listening thread
        input_thread = threading.Thread(target=self.receive_message)
        input_thread.start()

        # Start the child process in a separate thread
        child_thread = threading.Thread(target=self.run_child_process)
        child_thread.start()

        child_thread_live_simulation = threading.Thread(target=self.live_simulation)
        # Join threads at the end
        if self.is_debug:
            child_thread_live_simulation.start()
            child_thread_live_simulation.join()
        input_thread.join()
        child_thread.join()


if __name__ == "__main__":
    ipc = InterprocessCommunication()
    args = sys.argv[1:]
    try:
        ipc.run(args)
    except KeyboardInterrupt:
        print("Interrupt received, stopping child process...")
        print('Child process Exited!')
        sys.exit(0)
