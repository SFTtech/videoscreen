Videoscreen
===========

Listens on a TCP port for incoming media urls.

The url is opened with mpv and played.

Another url terminates the previous link.

Optionally, `mpd` can be paused during playback when using `-m`.


Invocation
----------

Try invoking with `--help` to see usage and configuration information.

```
python3 -m videoscreen -- --fs
```

Options after the `--` are passed to mpv.


License
-------

This tool is licensed under:

`GNU Affero General Public License v3 or later`.

See [copying.md](copying.md) and [LICENSE](LICENSE) for further information.
