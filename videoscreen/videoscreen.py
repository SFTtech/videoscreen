"""
The video screen.
"""

import asyncio
import re

from .mpd import MPD
from .player import Player


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

        self.connection_count = 0
        self.last_played_seq_id = -1

    def get_play_id(self):
        """ return the connection sequence number """
        ret = self.connection_count
        self.connection_count += 1
        return ret

    def is_newest_id(self, seq_nr):
        """ return if the given sequence number """
        return seq_nr > self.last_played_seq_id

    def display(self, seq_nr, sender, data):
        """
        show a new video and kill the old one
        TODO: player selection e.g. for jpgs
        """

        if not self.is_newest_id(seq_nr):
            return b"can't play expired connection id\n"

        self.last_played_seq_id = seq_nr

        if self.mpv is not None:
            self.mpv.kill()
            self.mpv.join()

        if data:
            print("{} showing '{}'".format(sender, data))
            self.mpv = Player(MPV_INVOCATION + self.mpv_options + ["--", data],
                              self.on_player_launch, self.on_player_terminate)
            self.mpv.start()
        else:
            print("{} stopped video".format(sender))

        return b"yay!\n"

    def on_player_launch(self):
        """ what to do right before the player starts """
        if self.control_mpd:
            self.mpd_was_playing = self.mpd.pause()

    def on_player_terminate(self):
        """ what to do when the videoscreen player terminates """
        if self.control_mpd and self.mpd_was_playing:
            self.mpd.play()

    async def process_command(self, cmd, connection_id, peer_id):
        """
        Process a command from a client
        """

        cmdstr = cmd.decode(errors="ignore").strip()
        command = cmdstr.split()

        if command and command[0] == "help":
            return (
                False,
                ("-=[videoscreen]=-\n"
                 "help - help\n"
                 "vol [+-=]$percent - volume control\n"
                 "anything else - play media\n").encode()
            )

        elif command and command[0].startswith("vol"):
            # vol (=)50|vol +12|vol -10
            if len(command) == 2:
                vol_cmd = re.match(r"([+=-]?)\s*(\d+)", command[1])
                if vol_cmd:
                    op = vol_cmd.group(1).replace("=", "")
                    vol = min(int(vol_cmd.group(2)), 100)

                    cmd = ["amixer", "sset", "Master", "{}%{}".format(vol, op)]
                    proc = await asyncio.create_subprocess_exec(*cmd)

                    ret = b"kay\n" if (await proc.wait() == 0) else b"fail\n"
                    return (False, ret)

            return (False, b"invalid volume command\n")

        elif command and command[0] == "exit":
            return (True, b"kthxbai\n")

        else:
            ret = self.display(connection_id, peer_id[0], cmdstr)
            return (True, ret)

    async def new_client(self, reader, writer):
        """
        Called when a new client connects to the server.
        """

        conn_id = self.get_play_id()
        peer_id = writer.get_extra_info("peername")

        while True:
            command = await reader.readline()

            if not command:
                writer.write(b"cya\n")
                reader.feed_eof()
                writer.close()
                break

            try:
                do_close, result = await self.process_command(
                    command, conn_id, peer_id
                )

                writer.write(result)

                if do_close:
                    writer.close()
                    break

            except Exception as exc:
                import traceback
                traceback.print_exc()
                writer.write(("error: %s\n" % exc).encode())

    def launch(self):
        """ run the videoscreen """

        print("launching on {}:{}...".format(self.address, self.port))

        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.new_client,
                                    self.address, self.port)
        server = loop.run_until_complete(coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
