"""
protocol definition for data reception
"""

import asyncio


class UrlReceiver(asyncio.Protocol):
    """
    protocol for receiving the media url
    """

    MAX_WAIT = 10
    LINEBUF_MAX = 4096

    def __init__(self, screen):
        self.buf = bytearray()
        self.screen = screen
        self.transport = None
        self.peername = None
        self.timer = None

    def connection_made(self, transport):
        self.seq_nr = self.screen.get_play_id()

        self.peername = transport.get_extra_info('peername')
        self.transport = transport
        loop = asyncio.get_event_loop()
        self.timer = loop.call_later(self.MAX_WAIT, self.timeout)

    def data_received(self, data):
        if len(self.buf) + len(data) > self.LINEBUF_MAX:
            self.transport.write(b"too much!\n")
            self.close()
            return

        if not self.screen.is_newest_id(self.seq_nr):
            self.transport.write(b"too slow!\n")
            self.close()
            return

        self.buf += data

        # a url is \n-terminated
        npos = self.buf.find(b"\n")
        if npos != -1:
            self.timer.cancel()

            self.transport.write(b"yay!\n")
            self.transport.close()

            data = self.buf[:npos]
            self.screen.display(self.seq_nr, self.peername, data.decode())

    def timeout(self):
        """ no answer for some time """
        self.transport.write(b"too late!\n")

    def close(self):
        """ cancel the timer and close the connection """
        if self.timer:
            self.timer.cancel()
        self.transport.close()

    def connection_lost(self, exc):
        pass
