import soundfile as sf
import numpy as np
import spicy
import matplotlib.pyplot as plt

def getEnveloppe(data, N, K):
    h = np.ones(K) * (1 / K)
    enveloppe = np.convolve(h, abs(data))
    return enveloppe[0:N]
def ReadWavFile(filePath):
    if '.wav' not in filePath:
        raise Exception('this file is not an .wav file')
    data, fe = sf.read(filePath)
    N = len(data)
    return data, fe, N

def getKByAmplitude(amplitudeCible, frequenceCoupure):
    k = 1
    gain = 1
    while not (amplitudeCible - 0.001 < gain < amplitudeCible + 0.001):
        gain = (1 / k) * np.sin(frequenceCoupure * k / 2) / np.sin(frequenceCoupure / 2)
        k += 1
    if(k % 2 == 0):
        return k+1
    else:
        return k

def get32PrimarySinusParams(data, fe, N):
    # on trouve le gain et la phase sur la longueur de l'échantillon
    X = np.fft.fft(data)
    gain = np.abs(X)
    phase = np.angle(X)
    # on trouve les peaks du signal
    peaks = spicy.signal.find_peaks(X, distance=1600)
    peaks32 = peaks[0][0:32]

    gains = []
    phases = []
    freqs = []
    for i in range(0, 32):
        # f = fe * m / N
        freqs.append((peaks32[i] * fe) / N)
        # on va chercher la phase au m correspondant
        phases.append(phase[(peaks32[i])])
        # on va chercher le gain au m correspondant
        gains.append(gain[(peaks32[i])])
    return freqs, phases, gains

def createSound(freqs, phases, gains, facteur, temps):
    sound = np.zeros(len(temps))
    for i in range(0, 32):
        sound += gains[i] * np.sin(2 * np.pi * freqs[i] * facteur * temps + phases[i])
    sound = sound / max(gains)
    return sound

def combineEnveloppeSound(enveloppe,sound):
    return (sound*enveloppe) /max(enveloppe)
