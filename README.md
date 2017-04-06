# Dronetect

Dronetect is a Python/ Java framework for detecting drones (quadcopters) in YouTube videos, created initially for the TU Delft TI-2716-C Multimedia Analysis course. 

The framework is capable of:

1) Downloading YouTube videos from either a specific video ID (e.g. `YY3AhuP0BRU`) or a text query (e.g. `DJI Phantom 4`),
1) Splitting `.mp4` YouTube videos into n-millisecond clips, and converting them to separate `.avi` video and `.wav` audio files,
1) Playing back the `.avi` and `.wav` components together in an environment that allows the user to efficiently put category labels on each clip,
1) Storing these labels in a database,
1) Analyzing the audio in each clip to automatically label it as drone, and
1) Evaluating its own performance against the labels in the database to calculate precision and recall.

The categories in which the video clips are sorted are:

* **Category 1**: 3-rd person drone videos with sound (videos taken _of_ a drone, with the sound of the drone)
* **Category 2**: 1-st person drone videos with sound (videos taken _by_ a drone, with the sound of the drone)
* **Category 3**: Trash (everything else)

Dronetect consists of several components:

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

The database is used to store labels generated using the labeling script, and used by the classifier to evaluate its own performance. It consists of a single `classifications` table:

```sql
CREATE TABLE IF NOT EXISTS classifications (
    video_id        TEXT    NOT NULL,
    start_time_ms   INTEGER NOT NULL,
    category        INTEGER NOT NULL CHECK (category >= 1 AND category <= 3),

    PRIMARY KEY (video_id, start_time_ms)
);
```

The columns are:
* `video_id`: The YouTube video ID (e.g. `dQw4w9WgXcQ`)
* `start_time_ms`: The time in the video at which this clip starts, in milliseconds (e.g. `2500`)
* `category`: The category, which can be `1`, `2`, or `3`

## Labeling Script

The labeling script is written in Python and called `label_data.py`. It connects to the database and then starts iterating over the video clips in the provided folder. If both a `.wav` and `.avi` are available for a video ID, the script checks whether the clip was already labeled. If it was, it's skipped. Otherwise, the script plays the video and audio and presents the user is with the following options:

* Label clip as **Category 1**
* Label clip as **Category 2**
* Label clip as **Category 3**
* Rewatch the clip
* Save and quit

Once the user calls the "Save and quit" option, the labels are saved to the database.

### Setup

Install dependencies:

```bash
sudo apt-get install python-pygame
```
### Usage

Navigate to the Python source folder and run the script, passing the path to the folder of video clips you want to label as well as the location of the database you want to write to.

```bash
cd src/main/python
python label_data.py /path/to/Videos path/to/database.db
```

Follow the instructions in the terminal. Make sure to use `q` to quit, so your labels are saved to the database!

## Classifier

[TO DO]
