"""
protocol definition for data reception
"""

import asyncio


class UrlReceiver(asyncio.Protocol):
    """
    protocol for receiving the media url
    """

    def __init__(self, screen):
        self.buf = bytearray()
        self.screen = screen
        self.transport = None
        self.peername = None

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        self.buf += data

        # a url is \n-terminated
        npos = self.buf.find(b"\n")
        if npos != -1:
            data = self.buf[:npos]
            self.screen.display(self.peername, data.decode())

            self.transport.write(b"yay!\n")
            self.transport.close()
