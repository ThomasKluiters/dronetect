# Dronetect

Dronetect is a Python/ Java framework for detecting drones (quadcopters) in YouTube videos, created initially for the TU Delft TI-2716-C Multimedia Analysis course. 

The framework is capable of:

1) Downloading YouTube videos from either a specific video ID (e.g. `YY3AhuP0BRU`) or a text query (e.g. `DJI Phantom 4`),
1) Splitting `.mp4` YouTube videos into n-millisecond clips, and converting them to separate `.avi` video and `.wav` audio files,
1) Playing back the `.avi` and `.wav` components together in an environment that allows the user to efficiently put category labels on each clip,
1) Storing these labels in a database,
1) Analyzing the audio in each clip to automatically label it as drone, and
1) Evaluating its own performance against the labels in the database to calculate precision and recall.
