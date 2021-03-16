import numpy as np
import scipy as sp
from scipy.io.wavfile import read
from scipy.fftpack import rfft, irfft, fftfreq, fft
from scipy.signal import butter, lfilter

import matplotlib.pyplot as plt
import numpy as np


fs,xx = read('../input/SuperCoilsEN_audio/SuperCoilsEN_noise.wav')

n = len(xx)
x = np.linspace(0.0, (n-1)*fs, n)
#get Fourier Transform of signal
yf = fft(xx)
mean = np.mean(yf)
print(mean)
#evenly spaced values of input signal over specifed interval
xf = np.linspace(0.0, 1.0/(2.0*fs), n/2)

#compute 1-D discrete fourier transform
f_signal = rfft(xx)
#returns dft sample frequencies
print(len(xx))
W = fftfreq(len(xx),d=x[1]-x[0])
print(W)
cut_f_signal = f_signal.copy()
# filter all frequencies below the mean of all frequencies
# do this to filter out higher frequencies which are most likely noise
print(len(cut_f_signal))
# for i, val in enumerate(W):
#     if cut_f_signal[val] < mean:
#         cut_f_signal[i] = 0

cut_f_signal[(W<mean)] = 0


#return discrete fourier transform back into sequence
cut_signal = irfft(cut_f_signal)


# plt.plot(data)
# plt.title('Original Signal Spectrum')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Amplitude')
# plt.show()
#
# dt = 0.001
# n = len(data)
# #getting the fourier transform of the inpput signal
# ft = np.fft.fft(data,n)
#
# PSD = (ft * np.conj(ft))/n
# freq = (1/(dt*n)) *np.arange(n)
# L= np.arange(1,np.floor(n/2), dtype='int')
#
# # fig, axs = plt.subplots(2,1)
# # plt.sca(axs[0])
# plt.plot(freq, PSD, color = 'c', label='Noisy')
# plt.xlim(freq[L[0]], freq[L[-1]])
# plt.legend()
# plt.plot()
#
# indices = PSD >30
# PsdCleam = PSD*indices
# FourierTransformation = indices*ft
# ffilt = np.fft.ifft(FourierTransformation)
#
# #getting evenly spaced samples over the data interval
# scale = np.linspace(0, fs, len(data))

# plt.plot(scale[0:5000], np.abs(ffilt[0:5000]), 'r')
# plt.plot(ffilt)
# plt.title('Signal spectrum after FFT')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Amplitude')
# plt.show()

# #applying white noise to the signal
# #we do that to even out the noise of the signal
# GuassianNoise = np.random.randn(len(FourierTransformation))
#
# newSignal = GuassianNoise + data

#applying a high pass filter on the signal
b,a = butter(5, 1500/(fs/2), btype='highpass')

filteredSignal = lfilter(b,a,cut_signal)
plt.plot(filteredSignal) # plotting the signal.
plt.title('Highpass Filter')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Amplitude')
plt.show()
#
#
c,d = butter(5, 300/(fs/2), btype='lowpass') # ButterWorth low-filter
newFilteredSignal = lfilter(c,d,filteredSignal) # Applying the filter to the signal
plt.plot(newFilteredSignal) # plotting the signal.
plt.title('Lowpass Filter')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Amplitude')
plt.show()
zf = fft(newFilteredSignal)
tf = np.linspace(0.0, 1.0/(2.0*fs), n/2)
f, axarr = plt.subplots(1, 2, figsize=(9, 3))


axarr[0].plot(xf, 2.0/n * np.abs(yf[:n//2]))
axarr[0].set_xlabel("f")
axarr[0].set_ylabel("amplitude")

axarr[1].plot(tf, 2.0/n * np.abs(zf[:n//2]))
axarr[1].set_xlabel("f")
axarr[1].set_ylabel("amplitude")

plt.show()




audio = sp.io.wavfile.write('../input/SuperCoilsEN_audio/blub.wav',fs, newFilteredSignal)