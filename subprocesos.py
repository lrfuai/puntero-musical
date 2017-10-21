#!/usr/bin/env python 
 
import subprocess 
import os


 
process = subprocess.Popen(['python', "speech_to_text.py","hola"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
proc2 = subprocess.Popen(['python', 'play_tone.py', 'DO'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
proc3 = subprocess.Popen(['python', 'play_midi.py', 'DO'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


remainder = process.communicate()[0]
str2 = str(remainder.decode('utf-8'))
print (str2)
#stdout,stderr = process.communicate()
#print ( stdout)
#print ( stderr)

os.system ("python speech_to_text.py 'hola'")