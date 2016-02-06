"""
Contains the a media player
"""

import subprocess
from threading import Thread


class Player(Thread):
    """
    Player wrapper to detect its termination.
    """
    def __init__(self, cmd, start_hook=None, stop_hook=None):
        super().__init__()

        self.cmd = cmd
        self.proc = None
        self.start_hook = start_hook
        self.stop_hook = stop_hook

    def run(self):
        if self.start_hook:
            self.start_hook()

        self.proc = subprocess.Popen(self.cmd)
        self.proc.wait()

        if self.stop_hook:
            self.stop_hook()

    def kill(self):
        """ kill the contained process """
        if self.proc:
            try:
                self.proc.wait(timeout=0.1)
                return
            except subprocess.TimeoutExpired:
                self.proc.kill()

            try:
                self.proc.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                raise Exception("process doesn't die :(")
