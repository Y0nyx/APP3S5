import matplotlib.pyplot as plt
import numpy as np

def plotSpectreDBOriginal (x, fe):
    n = np.arange(-len(x)/2, len(x)/2)
    W = np.hanning(len(x))
    X = np.fft.fftshift(np.fft.fft(x * W))
    X_DB = 20 * np.log10(np.abs(X))
    freqs = ((n * fe) / len(x))
    plt.plot(freqs[80000:160000], X_DB[80000:160000])
    plt.title("Spectre de Fourrier du LA dièse Original")
    plt.ylabel("Amplitude en DB")
    plt.xlabel("Fréquence en Hz")
    plt.show()

def ComparaisonSyntheseVsOriginal (Synthese, Original, fe):
    n = np.arange(0, len(Synthese) / 2)
    freqs = ((n * fe) / len(Synthese))

    #Original
    W = np.hanning(len(Original))
    X_Original = np.fft.fftshift(np.fft.fft(Original * W))
    X_DB_Original = 20 * np.log10(np.abs(X_Original))

    #Synthese
    X_Synthese = np.fft.fftshift(np.fft.fft(Synthese))
    X_DB_Synthese = 20 * np.log10(np.abs(X_Synthese))

    plt.subplot(2, 1, 1)
    plt.plot(freqs, X_DB_Original[80000:160000])
    plt.title("Spectre de Fourrier du LA dièse original")
    plt.ylabel("Amplitude en DB")
    plt.subplot(2, 1, 2)
    plt.plot(freqs, X_DB_Synthese[80000:160000])
    plt.title("Spectre de Fourrier du LA dièse synthétisé")
    plt.ylabel("Amplitude en DB")
    plt.xlabel("Fréquence en Hz")
    plt.show()

def ComparaisonSyntheseVsOriginalBasson (Synthese, Original, fe):
    n_Original = np.arange(0, len(Original) / 2)
    freqs_Original = ((n_Original * fe) / len(Original))

    n_Synthese = np.arange(0, len(Synthese) / 2)
    freqs_Synthese = ((n_Synthese * fe) / len(Synthese))

    # Original
    W = np.hanning(len(Original))
    X_Original = np.fft.fftshift(np.fft.fft(Original * W))
    X_DB_Original = 20 * np.log10(np.abs(X_Original))

    # Synthese
    X_Synthese = np.fft.fftshift(np.fft.fft(Synthese))
    X_DB_Synthese = 20 * np.log10(np.abs(X_Synthese))

    plt.subplot(2, 1, 1)
    plt.plot(freqs_Original, X_DB_Original[int(len(Original)/2):int(len(Original))])
    plt.title("Spectre de Fourrier du son de basson original")
    plt.ylabel("Amplitude en DB")
    plt.subplot(2, 1, 2)
    plt.plot(freqs_Synthese, X_DB_Synthese[int(len(Synthese)/2):int(len(Synthese))])
    plt.title("Spectre de Fourrier du son de basson synthétisé")
    plt.ylabel("Amplitude en DB")
    plt.xlabel("Fréquence en Hz")
    plt.show()

def plotEnveloppeTemporel (enveloppe, title, axeY, axeX):
    plt.plot(enveloppe)
    plt.title(title)
    plt.ylabel(axeY)
    plt.xlabel(axeX)
    plt.show()

def plotReponseImplusionnelTemporel (data, title, axeY, axeX):
    m = np.arange(0, len(data) / 2)
    dataDb = 20 * np.log10(np.abs(data))
    omega = 2 * np.pi * m / len(data)
    plt.plot(omega, dataDb[80000: 160000])
    plt.title(title)
    plt.ylabel(axeY)
    plt.xlabel(axeX)
    plt.show()

def plotReponseImplusionnelFrequenciel (data, title, axeY, axeX):
    m = np.arange(-len(data) / 2, len(data) / 2)
    dataDb = 20 * np.log10(np.abs(data))
    omega = 2 * np.pi * m / len(data)
    plt.plot(omega, dataDb)
    plt.title(title)
    plt.ylabel(axeY)
    plt.xlabel(axeX)
    plt.show()

def plotPhase (data, title, axeY, axeX):
    m = np.arange(-len(data) / 2, len(data) / 2)
    omega = 2 * np.pi * m / len(data)
    plt.plot(omega, data)
    plt.title(title)
    plt.ylabel(axeY)
    plt.xlabel(axeX)
    plt.show()

def plotSinus (data, title, axeY, axeX):
    plt.plot(data)
    plt.title(title)
    plt.ylabel(axeY)
    plt.xlabel(axeX)
    plt.show()

def plotSinusComparative(data1,data2, title, axeY, axeX):
    plt.plot(data1)
    plt.plot(data2)
    plt.title(title)
    plt.ylabel(axeY)
    plt.xlabel(axeX)
    plt.show()