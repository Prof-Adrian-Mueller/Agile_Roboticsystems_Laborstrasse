import subprocess
from PyQt6.QtCore import QThread, pyqtSignal
import select


class SubprocessThread(QThread):
    outputReceived = pyqtSignal(str)
    errorReceived = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, text=True, bufsize=1, universal_newlines=True)
            output = ""
            error = ""
            while True:
                reads = [self.process.stdout.fileno(), self.process.stderr.fileno()]
                ret = select.select(reads, [], [])

                for fd in ret[0]:
                    if fd == self.process.stdout.fileno():
                        out_char = self.process.stdout.read(1)
                        if out_char == '\n':
                            self.outputReceived.emit(output.strip())
                            output = ""
                        else:
                            output += out_char
                    if fd == self.process.stderr.fileno():
                        err_char = self.process.stderr.read(1)
                        if err_char == '\n':
                            self.errorReceived.emit(error.strip())
                            error = ""
                        else:
                            error += err_char
                if self.process.poll() is not None:
                    break
        except Exception as e:
            self.errorReceived.emit(str(e))

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()