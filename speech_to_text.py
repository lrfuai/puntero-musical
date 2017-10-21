import sys
import pyttsx3

# Get the arguments list 
cmdargs = sys.argv[1:]  #[1:] es para que lea solo el texto despues del nombre del scrip

x = pyttsx3.init()
x.setProperty('rate', 130)

##  voices = x.getProperty('voices')
##    for voice in voices:
##        print ("Using voice:", repr(voice))
x.setProperty('voice', '0x03A7FE90')
x.say(cmdargs)
x.setProperty('volume',0.9) 
x.runAndWait()
#print (cmdargs)
#user_args = sys.argv[1:] # get everything after the scrip)
#print    (user_args)

