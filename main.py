import numpy as np
import matplotlib.pyplot as plt
import SignalsManager as sm
import soundfile as sf

# Constantes
pi = np.pi

#-------------------------------------------------------------------------
# Problème 1: Synthèse d'un partition de beethoven
#-------------------------------------------------------------------------

# Constantes pour le problème de synthèse de signaux
gainCible = -3
amplitudeCible = 10 ** (gainCible/20)
frequenceCoupure = pi / 1000

facteurSOL = 0.891
facteurMIbemol = 0.749
facteurFA = 0.794
facteurRe = 0.667

# Get les données nécessaire à la synthèse
data, fe, N = sm.ReadWavFile('./Signals/note_guitare_LAd.wav')
K = sm.getKByAmplitude(amplitudeCible, frequenceCoupure)
freqs, phases, gains = sm.get32PrimarySinusParams(data, fe, N)
enveloppe = sm.getEnveloppe(data, N, K)

temps = np.arange(0, N / fe, 1 / fe)

# Synthèse des signaux nécessaire
SOL = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurSOL, temps)
MIbemol = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurMIbemol, temps)
Silence = np.zeros(N)
FA = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurFA, temps)
RE = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurRe, temps)

# Création de la partition
beethoven = []
beethoven.extend(SOL)
beethoven.extend(SOL)
beethoven.extend(SOL)
beethoven.extend(MIbemol)
beethoven.extend(Silence)
beethoven.extend(FA)
beethoven.extend(FA)
beethoven.extend(FA)
beethoven.extend(RE)

# Créer le dossier .wav de la partition
sf.write("./SignalsSynthese/beethoven.wav", beethoven, fe, 'PCM_24')

#-------------------------------------------------------------------------
# Problème 2: Éliminer la sinusoïdade à 1000 hz
#-------------------------------------------------------------------------

data2, fe2, N2 = sm.ReadWavFile('./Signals/note_basson_plus_sinus_1000_Hz.wav')
N2 = 6000
K2 = 81
n = np.arange(0, N2)
g = [0] * (N2)
g[0] = 1

h2 = (1 / N2) * np.sin(np.pi * n * K2 / N2) / (np.sin(np.pi * n / N2) + 1e-20)
H2 = np.fft.fft(h2)

hcoupebande = g - (2*h2*np.cos(2*pi*1000*n/fe2))
Hcoupebande = np.fft.fft(hcoupebande)

response = np.convolve(data2, hcoupebande)

#plt.plot(temps2, data2)
#plt.plot(temps2, response)
#plt.show()

plt.subplot(3, 1, 1)
plt.stem(h2)
plt.subplot(3, 1, 2)
plt.stem(np.abs(H2))
plt.subplot(3, 1, 3)
plt.stem(response)
plt.show()

sf.write("./SignalsSynthese/response2.wav", response, fe2, 'PCM_24')

# extra
m = np.arange(- N/2, N/2, 1)
W = 2*np.pi*m/N
h_passebas = (1/K) * np.sin(W*K/2)/(np.sin(W/2) + 1e-20)

