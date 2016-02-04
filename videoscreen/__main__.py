#!/usr/bin/env python3

"""
videoscreen launcher
"""

import argparse

from . import VideoScreen

def main():
    """ launch the screen """

    cli = argparse.ArgumentParser()
    cli.add_argument("-p", "--port", default=60601,
                     type=int, help="port to listen on")
    cli.add_argument("-l", "--listen", default="0.0.0.0",
                     help="ip to listen on")

    args = cli.parse_args()

    screen = VideoScreen(args.listen, args.port)
    screen.launch()

if __name__ == "__main__":
    main()
