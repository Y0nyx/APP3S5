import soundfile as sf

def ReadWavFile (filePath):
    if '.wav' not in filePath:
        raise Exception('this file is not an .wav file')
    return sf.read(filePath)