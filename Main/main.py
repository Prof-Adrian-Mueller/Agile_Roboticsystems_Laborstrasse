import subprocess
import sys
import time
import threading

class InterprocessCommunication:
    def __init__(self, is_debug=True):
        self.is_debug = is_debug

    def send_message(self, message):
        sys.stdout.write(f"Sending message: {message}\n")
        sys.stdout.flush()

    def receive_message(self):
        line = sys.stdin.readline().strip()
        sys.stdout.write(f"Received message: {line}\n")
        sys.stdout.flush()
        return line

    def run_child_process(self):
        if self.is_debug:
            sys.stdout.write("INPUT ANZAHL_TUBES\n")
            sys.stdout.flush()

            while True:
                received_message = self.receive_message()

                if received_message == 'exit':
                    print('Child process Exited!')
                    sys.exit(0)

    def run(self):
        if self.is_debug:
            print("E&T Started!")

            # Start the child process in a separate thread
            child_thread = threading.Thread(target=self.run_child_process)
            child_thread.start()

            self.send_message("exit")
            child_thread.join()

        else:
            from Main.doBot_Steuerung import steuerung
            print("Starting steuerung")
            steuerung()

if __name__ == "__main__":
    ipc = InterprocessCommunication()

    try:
        ipc.run()
    except KeyboardInterrupt:
        print("Interrupt received, stopping child process...")
        ipc.worker_thread.stop_child_process()
