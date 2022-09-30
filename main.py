import numpy as np
import matplotlib.pyplot as plt
import SignalsManager as sm

data, fe = sm.ReadWavFile('./Signals/note_guitare_LAd.wav')
print(data, fe)
N = len(data)
n = np.arange(0, N)
K = 800

# Hanning
w = np.hanning(N)
dataHanning = w * data
# Magnitude
X = np.fft.fftshift(np.fft.fft(dataHanning))
X_mag = np.abs(X)
# Phase
X_phase = np.angle(X)

plt.plot(n, X_phase)
plt.show()
exit()

h = np.ones(K)*(1/K)


X_mag = np.abs(X)
X_phase = np.angle(X)

plt.subplot(3, 1, 1)
plt.stem(n, X)
plt.subplot(3, 1, 2)
plt.stem(n, X_mag)
plt.subplot(3, 1, 2)
plt.stem(n, X_phase)
plt.show()