from daemon import Daemon
import time
from TwitterAdapter import TwitterAdapter

class ClassicalRNNDaemon(Daemon):
    def run(self):
        twitter = TwitterAdapter()
        while True:
            twitter.updateStatus()
            time.sleep(1)
