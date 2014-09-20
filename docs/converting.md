Converting Audio to Video
=========================

This page contains self-contained instructions for creating a video
from an audio file.  These instructions are referenced in the
instructions for [Recording and Posting Meeting Audio](audio.md).

These instructions assume you have the following:

* an audio file (e.g. an MP3), and
* an image to display during the video (e.g. a PNG).

This document describes two methods that can be used:

* A more technical method using FFmpeg, and
* A less technical method for Mac OS X users using iMovie.

The FFmpeg method is much faster and more automated, but it requires
more technical knowledge (e.g. familiarity with the command-line).


Using FFmpeg
------------

This section contains alternate instructions for converting an
audio file to video, using the open-source command-line utility
[FFmpeg][ffmpeg].

This method requires a bit more technical savvy, but the process is _MUCH_
faster (both in the number of manual steps to carry out and in waiting
for the computer to process).

For example, for a 10-minute video, this method took only about 5 seconds
of computer processing time (compared to 10 minutes using iMovie).
Also, the resulting file was much smaller (about 1/6th the size, or
7MB vs 43MB).

Install FFmpeg using MacPorts:

    $ sudo port install ffmpeg

Run the following from the command-line (filling in correct INPUT
and OUTPUT file names):

    $ ffmpeg -i INPUT.mp3 -f image2 -loop 1 -r 2 -i INPUT.png \
      -shortest -c:a copy -c:v libx264 -crf 23 -preset veryfast OUTPUT.mp4

Notes on the command above:

* `-f image2` means to use the "image2 sequence" format,
* `-loop 1` means to loop over the input stream (for image streams),
* `-r 2` means 2 frames per second of the image, and
* `-shortest` means to use the shortest stream to determine when encoding
  should end.

See [here](http://superuser.com/a/538168) for more info and for where
this suggested syntax came from.


[ffmpeg]: https://www.ffmpeg.org/
