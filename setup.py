#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='videoscreen',
    version='1.0',
    description='play links submitted via netcat with mpv',
    long_description=(
        "A small daemon which waits for incoming media urls.\n"
        "These will be played with the mpv player.\n"
        "This allows people e.g. in Hackerspaces to submit links "
        "to watch on some projector."
    ),
    author='Jonas Jelten',
    author_email='jj@stusta.net',
    url='https://github.com/SFTtech/videoscreen',
    packages=['videoscreen'],
    license='AGPL3+',
    platforms=[
        'Linux',
    ],
    classifiers=[
        ("License :: OSI Approved :: "
         "GNU Affero General Public License v3 or later (AGPLv3+)"),
        "Topic :: Multimedia :: Video :: Display",
        "Topic :: Multimedia :: Sound/Audio :: Players",
    ],
)
