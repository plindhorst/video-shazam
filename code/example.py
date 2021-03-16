import numpy as np
import pandas as pd

from numpy.fft import *

import matplotlib.pyplot as plt
from scipy.io.wavfile import read

fs,xx = read('../input/SuperCoilsEN_audio/SuperCoilsEN_noise.wav')
a, s = read('../input/SuperCoilsEN_audio/SuperCoilsEN_1.wav')
b, si = read('../input/SuperCoilsEN_audio/SuperCoilsEN2.wav')

print(xx)
signals = np.array([xx,s,si])

def sample(signal, kernel_size):
    sampled = np.zeros((signal.shape[0], signal.shape[1], signal.shape[2]//kernel_size))
    for i in range(signal.shape[2]//kernel_size):
        begin = kernel_size * i
        end = min(kernel_size * (i + 1), signal.shape[2])
        sampled[:, :, i] = np.mean(signal[:, :, begin:end], axis=2)
    return sampled

def filter_signal(signal, threshold=1e8):
    fourier = rfft(signal)
    frequencies = rfftfreq(signal.size, d=20e-3/signal.size)
    fourier[frequencies > threshold] = 0
    return irfft(fourier)

sampled = sample(signals, 100)
filtered = filter_signal(signals[0, 0, :], threshold=1e3)
plt.figure(figsize=(15, 10))
plt.plot(xx, label='Raw')
plt.plot(filtered, label='Filtered')
plt.legend()
plt.title("FFT Denoising with threshold = 1e7", size=15)
plt.show()