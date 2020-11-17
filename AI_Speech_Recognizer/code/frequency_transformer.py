import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Read the audio file
sample_freq, signal = wavfile.read('spoken_word.wav')

# Normalize the values
signal = signal / np.power(2, 15) 

# Extract the length of the audio signal
signal_len = len(signal)

# Extract the half length
half_len = np.ceil((signal_len + 1) / 2.0).astype(np.int)

# Apply Fourier transform
signal_f = np.fft.fft(signal)

# Normalization
signal_f = abs(signal_f[0:half_len]) / signal_len

# Take the square
signal_f **= 2

# Extract the length of the frequency transformed signal
len_fts = len(signal_f)

# Adjust the signal for even and odd cases
if signal_len % 2:
    signal_f[1:len_fts] *= 2
else:
    signal_f[1:len_fts-1] *= 2

# Extract the power value in dB
signal_power = 10 * np.log10(signal_f)

# Build the X axis
x_axis = np.arange(0, len_half, 1) * (sample_freq / signal_len) / 1000.0

# Plot the figure
plt.figure()
plt.plot(x_axis, signal_power, color='black')
plt.xlabel('Frequency (kHz)')
plt.ylabel('Signal power (dB)')
plt.show()
