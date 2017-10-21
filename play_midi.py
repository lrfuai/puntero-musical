# import library ---------------------------------------------------------------
import pygame.midi
import time
import sys
 
# define all the constant values -----------------------------------------------
device = 0
instrument = 25 # http://www.ccarh.org/courses/253/handout/gminstruments/
note_Do = 48   # http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
note_Re = 50
note_Mi = 52
note_Fa = 53
note_Sol = 55
note_La = 57
note_Si = 58

volume = 127
wait_time = 0.5

def play_Nota(sNota):
    Notas = [("DO",48),("RE",50),("MI",52),("FA",53),("SOL",55),("LA",57),("SI", 58)]
    bEncontro=False
    for i in range(len(Notas)): 
        if(sNota == Notas[i][0]):        
            print (Notas[i][0])
            player.note_on(Notas[i][1], volume)
            time.sleep(wait_time)
            player.note_off(note_Do, volume)
            bEncontro = True
            break
    if not bEncontro:
       player.note_on(note_Do, volume)




cmdargs = sys.argv[1:]
 
# initize Pygame MIDI ----------------------------------------------------------
pygame.midi.init()
 
# set the output device --------------------------------------------------------
player = pygame.midi.Output(device)
 
# set the instrument -----------------------------------------------------------
player.set_instrument(instrument)
 
# play the notes ---------------------------------------------------------------

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


# close the device -------------------------------------------------------------
del player
pygame.midi.quit()