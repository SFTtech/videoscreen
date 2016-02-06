"""
The video screen.
"""

import asyncio
import subprocess

from .mpd import MPD
from .player import Player
from .urlreceiver import UrlReceiver

MPV_INVOCATION = ["mpv"]


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
        self.mpd = MPD(args.mpdhost, args.mpdport)
        self.mpd_was_playing = False

    def display(self, sender, data):
        """
        show a new video and kill the old one
        TODO: player selection e.g. for jpgs
        """

        if self.mpv is not None:
            self.mpv.kill()
            self.mpv.join()

        if data:
            print("%s showing '%s'" % (sender, data))
            self.mpv = Player(MPV_INVOCATION + self.mpv_options + ["--", data],
                              self.on_player_launch, self.on_player_terminate)
            self.mpv.start()
        else:
            print("%s stopped video" % (sender, ))

    def on_player_launch(self):
        """ what to do right before the player starts """
        if self.control_mpd:
            self.mpd_was_playing = self.mpd.pause()

    def on_player_terminate(self):
        """ what to do when the videoscreen player terminates """
        if self.control_mpd and self.mpd_was_playing:
            self.mpd.play()

    def launch(self):
        """ run the videoscreen """

        print("launching on %s:%d..." % (self.address, self.port))

        loop = asyncio.get_event_loop()
        coro = loop.create_server(lambda: UrlReceiver(self),
                                  self.address, self.port)
        server = loop.run_until_complete(coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
