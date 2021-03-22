import scipy as sp
from scipy.io.wavfile import read
from scipy.fftpack import fftfreq, fft, ifft
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import numpy as np

def reduce_Noise(audio, output):
    fs,xx = read(audio)

    n = len(xx)
    x = np.linspace(0.0, (n-1)*fs, n)
    #get Fourier Transform of signal
    f_signal = fft(xx)

    #compute 1-D discrete fourier transform
    mean = np.mean(f_signal)
    #returns dft sample frequencies over all frequencies found in x
    print(len(xx))
    W = fftfreq(len(xx),d=x[1]-x[0])

    cut_f_signal = f_signal.copy()
    # filter all frequencies below the mean of all frequencies
    # do this to filter out higher frequencies which are most likely noise
    print(len(cut_f_signal))

    cut_f_signal[(W<mean)] = 0

    #return discrete fourier transform back into sequence
    cut_signal = ifft(cut_f_signal)

    #applying a high pass filter on the signal
    b,a = butter(5, 1500/(fs/2), btype='highpass')

    # Applying the filter to the signal
    filteredSignal = lfilter(b,a,cut_signal)

    #applying a low pass filter on the signa;
    c,d = butter(5, 300/(fs/2), btype='lowpass')
    # Applying the filter to the signal
    newFilteredSignal = lfilter(c,d,filteredSignal)

    #evenly spaced values of input signal over specifed half the signal interval
    # xf = np.linspace(0.0, 1.0/(2.0*fs), n/2)
    # tf = np.linspace(0.0, 1.0/(2.0*fs), n/2)
    #
    # f, axarr = plt.subplots(1, 2, figsize=(9, 3))
    #
    # #plotting the amplitude over frequency for Fourier transformation
    # axarr[0].plot(xf, 2.0/n * np.abs(f_signal[:n//2]))
    # axarr[0].set_xlabel("f")
    # axarr[0].set_ylabel("amplitude")
    #
    # #plotting the resulted filtered signal
    # axarr[1].plot(tf, 2.0/n * np.abs(newFilteredSignal[:n//2]))
    # axarr[1].set_xlabel("f")
    # axarr[1].set_ylabel("amplitude")
    #
    # plt.show()

    #writing to a new audio file
    audio = sp.io.wavfile.write(output,fs, np.real(newFilteredSignal))
    return audio