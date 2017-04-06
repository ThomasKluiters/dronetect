# Dronetect

Dronetect is a Python/ Java framework for detecting drones (quadcopters) in YouTube videos, created initially for the TU Delft TI-2716-C Multimedia Analysis course. 

The framework is capable of:

1) Downloading YouTube videos from either a specific video ID (e.g. `YY3AhuP0BRU`) or a text query (e.g. `DJI Phantom 4`),
1) Splitting `.mp4` YouTube videos into n-millisecond clips, and converting them to separate `.avi` video and `.wav` audio files,
1) Playing back the `.avi` and `.wav` components together in an environment that allows the user to efficiently put category labels on each clip,
1) Storing these labels in a database,
1) Analyzing the audio in each clip to automatically label it as drone, and
1) Evaluating its own performance against the labels in the database to calculate precision and recall.

It consists of several components:

* A Java YouTube video downloader/ splitter
* A SQLite database of category labels
* A Python script for playing back clips and labeling them
* Several Python scripts to classify clips and evaluate classifier performance

The sections below describe each component in detail.

## Video Downloader

The video video downloader is written in Java. It uses the [youtube-dl command line tool](https://rg3.github.io/youtube-dl/) to download videos, and [ffprobe](https://ffmpeg.org/ffprobe.html) and [ffmpeg](https://ffmpeg.org/) to convert the videos into their `.wav` and `.avi` audio/ video components and split them into 500-millisecond clips.

It outputs both the whole video (in `/data`) and a directory (`/data/scenes/VideoID`) of `.wav` audio clips and `.avi` video clips, named `YouTubeID-starttime-endtime.wav` and `YouTubeID-starttime-endtime.avi` respectively. The clip starting 3 seconds into video [dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ), for example, would be saved as files `dQw4w9WgXcQ-3000-3500.wav` and `dQw4w9WgXcQ-3000-3500.avi`.

### Usage

To download a single YouTube video by its ID:

```bash
javac src/main/java/nl/drone/tect/Main.java
java Main.java dQw4w9WgXcQ
```

(If the URL of a video is `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, for example, the YouTube ID is `dQw4w9WgXcQ`.)

## Database

[TO DO]

## Labeling Script

[TO DO]

## Classifier

[TO DO]
