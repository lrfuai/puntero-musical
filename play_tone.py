#ejecuta una nota muscial que se envia con comando
# 16-10-2017
import sys
import pyaudio
import numpy as np
from time import sleep

def play_sound(frec):
    p = pyaudio.PyAudio()
    volume = 0.3     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = .600  # in seconds, may be float
    #f = 440.0        # sine frequency, Hz, may be float
    f = frec

    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32, channels=1,  rate=fs, output=True)
    # play. May repeat with different volume values (if done interactively) 
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_Nota(sNota):
    Notas = [("DO",261.63),("RE",293.66),("MI",329.63),("FA",349.23),("SOL",392),("LA",440),("SI", 493.98)]
    bEncontro=False
    for i in range(len(Notas)): 
        if(sNota == Notas[i][0]):        
            print (Notas[i][0])
            play_sound(Notas[i][1])
            bEncontro = True
            break
    if not bEncontro:
        play_sound(600)


cmdargs = sys.argv[1:]


if(len(cmdargs)==0):    
    play_Nota("DO")
    play_Nota("RE")
    play_Nota("MI")
    play_Nota("FA")
    play_Nota("SOL")
    play_Nota("LA")
    play_Nota("SI")    
else:
    sNota = str(cmdargs[0]).upper()
    print(cmdargs,sNota)
    play_Nota(sNota)