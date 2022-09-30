import spicy

def ReadWavFile (filePath):
    if '.wav' not in filePath:
        raise Exception('this file is not an .wav file')
    return spicy.io.wavfile.read(filePath)