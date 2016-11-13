import sys
import time
import argparse

from core import ClassicalRNNDaemon as rnnDaemon
from core import DAEMON_PID_FILE

def start(daemon):
    daemon.start()

def stop(daemon):
    daemon.stop()

def restart(daemon):
    daemon.restart()

def parseArgs():
    parser = argparse.ArgumentParser(description='ClassicalRNN Service')
    parser.add_argument('--start'   , action='store_const', const=lambda daemon:start(daemon)   , dest='run')
    parser.add_argument('--stop'    , action='store_const', const=lambda daemon:stop(daemon)    , dest='run')
    parser.add_argument('--restart' , action='store_const', const=lambda daemon:restart(daemon) , dest='run')

    return parser.parse_args()

def main():
    args = parseArgs()
    daemon = rnnDaemon(DAEMON_PID_FILE)
    args.run(daemon)

if __name__ == "__main__":
    main()
