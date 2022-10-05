import matplotlib.pyplot as plt
import numpy as np
import SignalsManager as sm
import PlotsManager as pm
import soundfile as sf
import math

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
son_guitare, fe_guitare, N_guitare = sm.ReadWavFile('./Signals/note_guitare_LAd.wav')
K = sm.getKByAmplitude(amplitudeCible, frequenceCoupure)
hanning = np.hanning(N_guitare)
freqs, phases, gains = sm.get32PrimarySinusParams(son_guitare*hanning, fe_guitare, N_guitare)
enveloppe = sm.getEnveloppe(son_guitare, N_guitare, K)

temps = np.arange(0, N_guitare / fe_guitare, 1 / fe_guitare)

# Synthèse des signaux nécessaire
SOL = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurSOL, temps)
MIbemol = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurMIbemol, temps)
Silence = np.zeros(N_guitare)
FA = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurFA, temps)
RE = enveloppe * sm.createSound32Sinus(freqs, phases, gains, facteurRe, temps)
LAdiese = enveloppe * sm.createSound32Sinus(freqs, phases, gains, 1, temps)

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
sf.write("./SignalsSynthese/beethoven.wav", beethoven, fe_guitare, 'PCM_24')

#-------------------------------------------------------------------------
# Problème 2: Éliminer la sinusoïdade à 1000 hz
#-------------------------------------------------------------------------

# extraction des paramètres de la note de basson
son_basson, fe_basson, N_basson = sm.ReadWavFile('./Signals/note_basson_plus_sinus_1000_Hz.wav')

# constantes
N_basson = 6000
K_basson = math.floor((((40 * N_basson) / fe_basson)*2)+1)
n = np.arange(0, N_basson)

# création du signal dirac
g = [0] * (N_basson)
g[0] = 1

# création de la fenêtre de hanning
Whanning = np.hanning(len(son_basson))

# création du passe-bas
h_passebas = (1 / N_basson) * np.sin(np.pi * n * K_basson / N_basson) / (np.sin(np.pi * n / N_basson) + 1e-20)
H_passebas = np.fft.fft(h_passebas)

# création du coupe-bande avec le passe-bas
h_coupebande = g - (2*h_passebas*np.cos(2*pi*1000*n/fe_basson))
H_coupebande = np.fft.fft(h_coupebande)

# passer le son de basson dans le filtre 3 fois
son_basson_clair = np.convolve(son_basson*Whanning, h_coupebande)
son_basson_clair = np.convolve(son_basson_clair, h_coupebande)
son_basson_clair = np.convolve(son_basson_clair, h_coupebande)

# Créer le file .wav du son de basson clair
sf.write("./SignalsSynthese/son_basson_clair.wav", son_basson_clair, fe_basson, 'PCM_24')

# Request graphique
#pm.plotSpectreDBOriginal(son_guitare, fe_guitare)
#pm.ComparaisonSyntheseVsOriginal(LAdiese, son_guitare, fe_guitare)
#pm.ComparaisonSyntheseVsOriginalBasson(son_basson_clair, son_basson, fe_basson)
#pm.plotEnveloppeTemporel(enveloppe, "Enveloppe Temporel du son de guitare", "Amplitude", "n (échantillon")

m = np.arange(- N_guitare/2, N_guitare/2, 1)
W_guitare = 2*np.pi*m/N_guitare
h_passebas = (1/K) * np.sin(W_guitare*K/2)/(np.sin(W_guitare/2) + 1e-20)
#pm.plotReponseImplusionnelTemporel(h_passebas, "Réponse impulsionnelle du filtre passe-bas", "Amplitude (db)", "W (rad/échantillon)")

enveloppe_basson = sm.getEnveloppe(son_basson_clair, len(son_basson_clair), K)
#pm.plotEnveloppeTemporel(enveloppe_basson[2000:160000], "Enveloppe Temporel du son de basson clair", "Amplitude", "n (échantillon)")

#pm.plotReponseImplusionnelFrequenciel(np.abs(np.fft.fftshift(np.fft.fft(h_coupebande))), "Amplitude du filtre coupe-bande", "Amplitude(db)", "W (rad/échantillon)")
#pm.plotReponseImplusionnelFrequenciel(h_coupebande, "Réponse Impulsionnel temporel du filtre coupe-bande", "Amplitude(db)", "W (rad/échantillon)")
pm.plotReponseImplusionnelTemporel(h_coupebande, "Réponse impulsionnelle du filtre coupe-bande", "Amplitude", "W (rad/échantillon)")
#pm.plotPhase(np.angle(np.fft.fftshift(np.fft.fft(h_coupebande))),"Phase du filtre coupe-bande", "Amplitude", "W (rad/échantillon)")

#pm.plotSinus(h_coupebande,"Sinus du filtre coupe-bande", "Amplitude", "n (échantillon)")
temps_Sinus = np.arange(0, N_guitare / fe_basson, 1 / fe_basson)
sinus1000Hz = np.sin(2 * np.pi * 1000 * temps_Sinus)
WhanningSinus = np.hanning(len(sinus1000Hz))
son_sinus_clair = np.convolve(sinus1000Hz, h_coupebande)
son_sinus_clair = np.convolve(son_sinus_clair, h_coupebande)
son_sinus_clair = np.convolve(son_sinus_clair, h_coupebande)
#pm.plotSinusComparative(sinus1000Hz, son_sinus_clair,"Sinus de 1000hz filtré et non filtré", "Amplitude", "n (échantillon)")

#pm.plotSinusComparative(son_basson, son_basson_clair,"Son du Basson filtré et non filtré", "Amplitude", "n (échantillon)")

# création du signal synthétisé du basson clair
basson = sm.get32PrimarySinusParams(son_basson_clair, N_basson, fe_basson)
freqs, phases, gains = sm.get32PrimarySinusParams(son_basson_clair, N_basson, fe_basson)
basson_synthese = sm.createSound32Sinus(freqs, phases, gains, 1, temps_Sinus)
#plt.plot(son_basson_clair)
#basson_synthese = enveloppe_basson[0:135051]*basson_synthese[0:135051]
plt.plot(basson_synthese)
sf.write("./SignalsSynthese/basson_synthese.wav", basson_synthese, fe_basson, 'PCM_24')
#plt.show()
