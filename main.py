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
facteurMIbemol = 0.707
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
beethoven.extend(SOL[0:27000])
beethoven.extend(SOL[0:27000])
beethoven.extend(SOL[0:27000])
beethoven.extend(MIbemol[0:80000])
beethoven.extend(Silence[0:27000])
beethoven.extend(FA[0:27000])
beethoven.extend(FA[0:27000])
beethoven.extend(FA[0:27000])
beethoven.extend(RE[0:80000])

# Créer le dossier .wav de la partition
sf.write("./SignalsSynthese/beethoven.wav", beethoven, fe, 'PCM_24')

#-------------------------------------------------------------------------
# Problème 2: Éliminer la sinusoïdade à 1000 hz
#-------------------------------------------------------------------------

# extraction des paramètres de la note de basson
son_basson, fe_basson = sm.ReadWavFile('./Signals/note_basson_plus_sinus_1000_Hz.wav')

# constantes
N_basson = 6000
K_basson = 81
n = np.arange(0, N_basson)

# création du signal dirac
g = [0] * (N_basson)
g[0] = 1

# création du passe-bas
h_passebas = (1 / N_basson) * np.sin(np.pi * n * K_basson / N_basson) / (np.sin(np.pi * n / N_basson) + 1e-20)
H_passebas = np.fft.fft(h_passebas)

# création du coupe-bande avec le passe-bas
h_coupebande = g - (2*h_passebas*np.cos(2*pi*1000*n/fe_basson))
H_coupebande = np.fft.fft(h_coupebande)

# passer le son de basson dans le filtre 3 fois
son_basson_clair = np.convolve(son_basson, h_coupebande)
son_basson_clair = np.convolve(son_basson_clair, h_coupebande)
son_basson_clair = np.convolve(son_basson_clair, h_coupebande)

# Créer le file .wav du son de basson clair
sf.write("./SignalsSynthese/son_basson_clair.wav", son_basson_clair, fe_basson, 'PCM_24')
