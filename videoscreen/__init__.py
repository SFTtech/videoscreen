"""
The video screen.
"""

import socket
import subprocess
from threading import Thread

MPV_INVOCATION = ["mpv"]


class Player(Thread):
    """
    Player wrapper to detect its termination.
    """
    def __init__(self, cmd, hook=None):
        super().__init__()

        self.cmd = cmd
        self.proc = None
        self.hook = hook

    def run(self):
        print("exec: %s" % self.cmd)
        self.proc = subprocess.Popen(self.cmd)
        self.proc.wait()

        if self.hook:
            self.hook()

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


class VideoScreen:
    """
    video screen state class
    """

    def __init__(self, args):
        self.address = args.listen
        self.port = args.port

        self.mpv = None
        self.mpv_options = args.options[1:]

        self.control_mpd = args.music

        self.sock = None

    def display(self, data):
        """ show a new video and kill the old one """

        print("  showing '%s'" % data)

        if self.control_mpd:
            print("pausing mpd...")
            subprocess.call(["mpc", "pause"])

        # kill the existing mpv:
        if self.mpv is not None:
            self.mpv.kill()

        self.mpv = Player(MPV_INVOCATION + self.mpv_options + ["--", data],
                          self.on_player_terminate)
        self.mpv.start()

    def on_player_terminate(self):
        """ what to do when the videoscreen player terminates """
        if self.control_mpd:
            print("resuming mpd...")
            subprocess.call(["mpc", "play"])

    def launch(self):
        """ run the videoscreen """

        print("launching on %s:%d" % (self.address, self.port))

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind((self.address, self.port))
        self.sock.listen(1)

        while True:
            (conn, addr) = self.sock.accept()
            print("new link from '%s'" % (addr,))

            buf = bytearray()

            while True:
                buf += conn.recv(2048)
                npos = buf.find(b"\n")
                if npos != -1:
                    data = buf[:npos]
                    self.display(data.decode())
                    conn.close()
                    break
