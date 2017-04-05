import cv2
import scipy.io.wavfile as wav
import sys
import audio

def process(videopath, audiopath, database):
    """Process a 2 second long video and decide if it is a category 2 scene"""
    
    cap = cv2.VideoCapture(videopath)
    samplerate, samples = wav.read(audiopath)
    
    audio_label = audio.process(samples, samplerate)
    
    if audio_label:
        return 1
    else:
        return 3
    
if __name__ == '__main__':
    if len(sys.argv) == 4:
        process(sys.argv[1], sys.argv[2], sys.argv[3])
