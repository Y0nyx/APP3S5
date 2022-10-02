# Probleme 2 procedural 3
import numpy as np
import matplotlib.pyplot as plt

# h[n] = (1/N) * sin(pi*n*K/N) / sin(pi * n/N)

N = 8
K = 3

n = np.arange(-int(N / 2), int(N / 2))
m = np.arange(-int(N / 2), int(N / 2))
h = (1 / N) * np.sin(np.pi * n * K / N) / (np.sin(np.pi * n / N) + 1e-20)
h[int(N / 2)] = K / N
H = np.fft.fftshift(np.fft.fft(h))
hpassehaut = ((-1.0) ** n) * h
Hpassehaut = np.fft.fftshift(np.fft.fft(hpassehaut))

t = np.arange(0, 100000) * (1 / 48000)
x = np.cos(2 * np.pi * 200 * t) + 0.2 * np.cos(2 * np.pi * 15000 * t)
y = np.convolve(x, h, mode='same')
y2 =  np.convolve(x, hpassehaut, mode='same')
xcible = np.cos(2 * np.pi * 200 * t)

#plt.plot(t, x)
#plt.plot(t, xcible)
#plt.plot(t, y)
#plt.show()
#exit()



plt.subplot(3,1,1)
plt.stem(n, h)
plt.subplot(3,1,2)
plt.stem(m, np.abs(H))
plt.subplot(3,1,3)
plt.stem(m, np.abs(Hpassehaut))
plt.show()