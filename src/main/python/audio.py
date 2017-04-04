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
    
    summed = [sum(x) for x in specs]
    band = [abs(x-5680)<250 for x in freqs]
    
    result = []
    score = 0
    for i in range(len(summed)):
        if band[i]:
            result.append(summed[i])
            score += summed[i]
        else:
            result.append(0)
    
    drone = score > 0.007
    print drone
    return drone
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        process(sys.argv[1], sys.argv[2])
