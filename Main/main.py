from multiprocessing import Process, Queue
import subprocess
import sys
import time

class MainClass:
    def __init__(self, DEBUG = True):
        try:
            from keyboard import is_pressed
        except ImportError:
            print("The 'keyboard' module is not installed. Installing now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
            from keyboard import is_pressed

        self.is_pressed = is_pressed
        self.DEBUG = DEBUG

    def run(self):
        if self.DEBUG:
            print("E&T Started!")
            sys.stdout.write("INPUT ANZAHL_TUBES")
            sys.stdout.flush()

            while True:
                time.sleep(5)
                # Send a message to the parent process
                sys.stdout.write("Hello from child process!\n")
                sys.stdout.flush()

                # Recieve message from the parent process
                line = sys.stdin.readline().strip()
                if not line:
                    break
                sys.stdout.write(f"Child received: {line}\n")
                sys.stdout.flush()

                # Check if 'q' is pressed
                if self.is_pressed('q'):
                    print('Program Exited!')
                    break

            print('Please enter "q" to exit.')
        else:
            from Main.doBot_Steuerung import steuerung
            print("Starting steuerung")
            steuerung()

if __name__ == "__main__":
    main_class = MainClass()
    main_class.run()


