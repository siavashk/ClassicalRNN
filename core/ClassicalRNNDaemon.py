from daemon import Daemon
import time

class ClassicalRNNDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)
