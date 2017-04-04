import sys
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram

def process(samples, f):
    #f, t, Sxx = signal.specgram(samples, f)
    #plt.pcolormesh(t, f, Sxx)
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
    #plt.show()
    
    print samples[:,0]
    specgram(samples[:,0], NFFT=256, Fs=f)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        process(sys.argv[1], sys.argv[2])
