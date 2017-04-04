import sys

from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import numpy as np

def process(samples, f):    
    if not isinstance(samples[0], np.int16):
        samples = samples[:,0]
    specs, freqs, t, x = specgram(samples, NFFT=256, Fs=f)
    specs /= np.sum(specs)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    
    summed = [sum(x) for x in specs]
    plt.plot(freqs, summed)
    plt.show()
    
    band = [abs(x-5680)<250 for x in freqs]
    
    result = []
    for i in range(len(summed)):
        if band[i]:
            result.append(summed[i])
        else:
            result.append(0)
            
    plt.plot(freqs, result)
    plt.show()
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        process(sys.argv[1], sys.argv[2])
