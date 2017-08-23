Videoscreen
===========

Listens on a TCP port for incoming media urls.

The url is opened with mpv and played.

Another url terminates the previous link.

Optionally, `mpd` can be paused during playback when using `-m`.


Dependencies
------------

* Python3
* [`mpv` player](https://mpv.io/)
* [`mpc` client](http://www.musicpd.org/clients/mpc/) (optional)


Invocation
----------

Try invoking with `python3 -m videoscreen --help` to see usage and configuration information.

```
python3 -m videoscreen -- --fs --quiet
```

All options after the `--` are passed to mpv.


systemd user service
--------------------

* Copy or symlink the `etc/videoscreen.service` to `~/.config/systemd/user/`
* Activate and launch it `systemctl --user enable --now videoscreen.service`


Usage
-----

The following commands can be issued to the host:

Command | What
--------|-----
`help` | show usage help
`$video_url` | play video url
`vol [+-=]$number` | change the system volume
`exit` | terminate connection


### Examples

Invoke the commands by sending to port `60601` of the host:

``` shell
# play a video
echo "$video_url" | nc $host $port

# change volume
echo "vol +13" | nc $host $port
echo "vol 33" | nc $host $port
echo "vol -37" | nc $host $port
```


License
-------

This tool is licensed under:

`GNU Affero General Public License v3 or later`.

See [copying.md](copying.md) and [LICENSE](LICENSE) for further information.
