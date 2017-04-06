# Python Processing

## Main

Syntax:

```bash
python main.py /path/to/video/folder /path/to/database.db
```

## Labeling

The `label_data.py` script is used to label testing/ training data into the following categories:

* Category 1: 3-rd person drone video with sound
* Category 2: 1-st person drone video
* Category 3: Trash

### Requirements

Install PyGame:

```bash
sudo pip install pygame
```

### Usage

```bash
python label_data.py /path/to/Videos path/to/database.db
```

Follow the instructions in the terminal. Make sure to use `q` to quit, so your labels are saved to the database!
