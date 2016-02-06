"""
mpd interaction
"""

import subprocess


class MPD:
    """
    represents the mpd state
    """

    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

    def is_running(self):
        """ test if mpd is playing """
        try:
            # parse the "[state]..." mpc output
            output = self.run_cmd("status")
            statusline = output.split(b"\n")[1]
            stoppos = statusline.find(b"]")
            status = statusline[1:stoppos]
            return status in {b"playing"}

        except IndexError:
            print("failed to check mpd status, assume stopped.")
            return False

    def pause(self):
        """
        pause the playback
        return if mpd was playing before the command
        """

        running = self.is_running()
        if running:
            print("pausing mpd...")
            self.run_cmd("pause")

        return running

    def play(self):
        """
        resume the playback
        return if mpd was playing before the command
        """

        running = self.is_running()
        if not running:
            print("playing mpd...")
            self.run_cmd("play")

        return running

    def run_cmd(self, cmd):
        """ run a mpd control command """

        call = ["mpc"]
        if self.host:
            call.extend(["--host", self.host])
        if self.port:
            call.extend(["--port", self.port])

        call.append(cmd)

        proc = subprocess.Popen(call, stdout=subprocess.PIPE)
        output, _ = proc.communicate()
        try:
            proc.wait(1)
        except subprocess.TimeoutExpired:
            raise Exception("mpc doesn't terminate!")

        return output
