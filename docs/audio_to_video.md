Creating a Video File from an Audio File
========================================

This document contains instructions for creating a video file from
an audio file.  This document is referenced in the parent document for
[Recording and Posting Meeting Audio](audio.md).

These instructions assume you have--

* an audio file (for example an MP3), and
* an image to display during the video (for example a PNG).

This document describes two different methods:

* the ["FFmpeg method"](#using-ffmpeg), which is more technical, and
* the ["iMovie method"](#using-imovie), which is for Mac OS X users
  and is less technical.

The FFmpeg method is _much_ faster and more automated than using iMovie,
but it requires more technical knowledge (e.g. familiarity with the
command-line).  Also, the FFmpeg method creates video files of a much
smaller size.

For example, for a 10-minute video, the FFmpeg method took only about
5 seconds of computer processing time (compared to 10 minutes using iMovie).
Also, the resulting file was about 1/6th the size, or 7MB vs 43MB.


Using FFmpeg
------------

This section contains instructions for creating a video file using the
open-source command-line utility [FFmpeg][ffmpeg].

This method requires a fair bit of technical knowledge.


### Install FFmpeg

First, install FFmpeg.  For example, on Mac OS X you can use install
FFmpeg using [MacPorts][macports] as follows:

    $ sudo port install ffmpeg


### Increase the Volume

    # Increase the volume by 1.5x.
    $ ffmpeg -i input.mp3 -af 'volume=1.5' output.mp3


### Combine files

If necessary, combine multiple files:

    $ ffmpeg -i concat:"part1.mp3|part2.mp3" -acodec copy audio_combined.mp3


### Convert audio to video

To create a video file from an audio file, run the following from the
command-line (filling in correct INPUT and OUTPUT file names):

    $ ffmpeg -i INPUT.mp3 -f image2 -loop 1 -r 2 -i INPUT.png \
      -shortest -c:a copy -c:v libx264 -crf 23 -preset veryfast \
      -movflags faststart OUTPUT.mp4

And then--

    $ ffmpeg -i INPUT.mp4 -acodec copy -vcodec copy OUTPUT.mkv


#### Notes on the commands above

Regarding the first command--

* `-f image2` means to use the "image2 sequence" format,
* `-loop 1` means to loop over the input stream (for image streams),
* `-r 2` means 2 frames per second of the image,
* `-shortest` means to use the shortest stream to determine when encoding
  should end, and
* `-movflags faststart` was added as an attempt to address a YouTube
  suggestion (see [here][streamable_encoding] for where the suggestion
  came from).

See [here](http://superuser.com/a/538168) for more info and for where
the suggested syntax came from.

The second command significantly speeds up YouTube processing time, and it
prevents the following YouTube warning from showing up after uploading
to YouTube:

> Your videos will process faster if you encode into a streamable file format.

This second command is advice taken from [here][streamable_encoding].


### Second approach

TODO: also try the following--

    $ ffmpeg -loop 1 -i image.jpg -i audio.mp3 -c:v libx264 \
      -c:a aac -strict experimental -b:a 192k -shortest output.mp4

(from http://www.labnol.org/internet/useful-ffmpeg-commands/28490/ )


Using iMovie
------------

These instructions were developed iMovie '09.  They are adapted from
YouTube's own help page [here][youtube-help].

Start iMovie (e.g. by clicking on it in the "Applications" folder).
Drag the MP3 audio file into the project area.  Also drag the image file
into the audio area.  The top of your iMovie window should now look
something like the following.  The green region corresponds to the
audio file, and the picture inside the green region corresponds to
the visual image.

![](images/imovie_01_initial_setup.png "iMovie - initial setup")

The imported image has a length of time associated to it
that says how long the image should display in the movie.
After dragging, this time starts out as 4 seconds, so you need to lengthen
the time of the image to match the length of the audio.

To confirm the length of the _audio clip_ in iMovie, click the green "gear"
in the upper left corner of the green box.  This lets you access
properties of the audio you imported.  Select "Clip Adjustments" in the
box that appears.

![](images/imovie_02_audio_properties.png "iMovie - Audio properties")

You should see a box appear that says, "Source Duration."  Note the time
duration somewhere.  This should match the duration of the original
trimmed audio you made in iTunes.

![](images/imovie_03_audio_duration.png "iMovie - Audio duration")

Now we will change the length of time of the image to match
the length of the audio.  To access the image properties, hover over the
image inside the green region.  A blue "gear" should appear in
the lower-left corner of the image.  Click the blue gear.

![](images/imovie_04_image_properties.png "iMovie - Image properties")

Now click "Clip Adjustments."  A dialog box should pop up that lets you
edit the image duration.

![](images/imovie_05_image_duration.png "iMovie - Image duration")

Set the duration of the image in the format `m:ss`.  Note that iMovie
seems to have an upper limit of 10 minutes for an image.
If the audio file is less than 10 minutes, set the image duration
equal to the duration of the audio.  Otherwise, set the image duration
equal to the maximum of 10:00.  We will address the audio after
10 minutes below.

Lengthening the image duration from 4 seconds to something longer
like 10 minutes might cause the green box to fill up the window as follows.

![](images/imovie_06_extend_image_duration.png "iMovie - Extend image duration")

If this occurs, change the "granularity" of the project view by moving
the bar in the lower-right corner of the project window all the way to
the right to "All."

![](images/imovie_07_granularity.png "iMovie - Project view granularity")

This should cause the green region to reduce back to its original size
of a single box.

By default, images imported into iMovie have a visual effect applied
to them called the "Ken Burns effect."  With this effect, the video
gradually zooms in to or out of the image over the course of the display
of the image.

To turn this feature off, hover over the image and click the blue gear
again.  This time, select "Cropping, Ken Burns & Rotation" in the menu
that pops up.  Some options should appear in the window on the right.
Select "Fit" and click "Done."  This will cause the image to remain still
over the course of its display.

![](images/imovie_08_turn_off_ken_burns.png "iMovie - Turn off Ken Burns")

If the audio file was less than 10 minutes long, you are done editing
the video.  More likely, the audio file was longer than 10
minutes long.  In this case, you need to create enough copies of
the 10-minute image to last the length of the audio.

To create enough copies of the image, click on the image so that a yellow
outline surrounds the image.  Press `COMMAND+C` to copy the image.
Then press `COMMAND+V` to paste enough copies of the 10-minute
image to span the length of the audio.  Double-check that each image
(except for the last) is exactly 10 minutes long.  You can do this by
hovering over each image.  For the last image, you should set the
duration so that it fills out the remaining length of the audio.

At this point, you are done editing and can create the final video file.
To do this, go to Share > "Export using QuickTime..."  This should
open a dialog box called "Save exported file as...".  The bottom of the
dialog box should look like the following:

![](images/imovie_09_export_dialog_box.png "iMovie - Export dialog box")


Click the "Options..." button next to "Export."  In the "Movie Settings"
dialog box, click the "Settings..." button in the "Video" section.
A dialog box like the following should appear.

![](images/imovie_10_video_compression.png "iMovie video compression settings")

Change the settings to match the settings in the picture above.
These settings are set to a lower quality to make the export faster, and
because a high quality is not needed for the video.

Click OK twice to close both dialog boxes, and then click save.
This will generate a ".mov" file, which is the video format for QuickTime
and is acceptable for YouTube.  Note that the export process may take a
relatively long time.  For example, a 10-minute video may take on the
order of 10 minutes to create.


[ffmpeg]: https://www.ffmpeg.org/
[macports]: https://www.macports.org/
[streamable_encoding]: http://hetzel.net/2014-01-29/youtube-videos-will-process-faster-encode-streamable-file-format/
[youtube-help]: https://support.google.com/youtube/answer/1696878?hl=en
