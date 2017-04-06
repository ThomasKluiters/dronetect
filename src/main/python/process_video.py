import cv2
import scipy.io.wavfile as wav
import sys
import audio
import video

def process(videopath, audiopath, database, sift_database):
    cap = cv2.VideoCapture(videopath)
    samplerate, samples = wav.read(audiopath)

    video_label = video.process(cap, sift_database)
    audio_label = audio.process(samples, samplerate)
    
    if audio_label and video_label:
        return 1
    elif audio_label and not video_label:
        return 2
    else:
        return 3
    
if __name__ == '__main__':
    if len(sys.argv) == 5:
        process(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
