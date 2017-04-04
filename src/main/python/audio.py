import sys
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram

def process(samples, f):    
    print samples
    specgram(samples, NFFT=256, Fs=f)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        process(sys.argv[1], sys.argv[2])
