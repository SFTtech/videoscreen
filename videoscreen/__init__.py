"""
The video screen.
"""

import socket
import subprocess

MPV_INVOCATION = ["mpv"]


class VideoScreen:
    """
    video screen state class
    """

    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.sock = None
        self.current_mpv = None

    def display(self, data):
        """ show a new video and kill the old one """

        print("  showing '%s'" % data)

        # kill the existing mpv:
        if self.current_mpv:
            try:
                self.current_mpv.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                self.current_mpv.kill()

            try:
                self.current_mpv.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                raise Exception("process doesn't die :(")

        self.current_mpv = subprocess.Popen(MPV_INVOCATION + [data])

    def launch(self):
        """ run the videoscreen """
        self.sock = socket.socket()
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
