# nestor balich 17-10--2017 Ok visita nuestro sitio en YOUTUBE -> NeoRoboticTV
# Twitter: nestorbalich (@nestorbalich) 
# genera un puntero en la posicion del dedo utilziado para apuntar
# al ponerlo sobre los botones genera un tono con la libreria midi de pygame
# openc se utiliza resta hull filtro blur y gausiano y deteccion de contornos
import cv2
import numpy as np
import math
import time
import pygame.midi

modo_Debugge = False

valSet = 90  #  BINARY threshold
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
pointRect = [(0.0),(0.0)]


#definiciones para pygame midi
device = 0

instrumento = 0 # http://www.ccarh.org/courses/253/handout/gminstruments/
vInstrumento = [("cesta",9),("Piano acustico",1),("Orngano de roca",19),("Guitarra acustica",25),("Bajo Electrico",33)\
,("sinfonica",55),("Trompeta",56),("Pajaro",123),("Redoblante",118),("Kalimba",113),("Violonchelo",43)]

volume = 127
#wait_time = 0.1
wait_cicle = 15      #espera ciclos para apagar la nota de mixer
count_cicle = 0
sNotaDet = ""

def play_Nota(sNota):
    global count_cicle
    global instrument
    global sNotaDet
    # http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
    Notas = [("DO",48),("RE",50),("MI",52),("FA",53),("SOL",55),("LA",57),("SI", 58)] 
   
    
    for i in range(len(Notas)): 
        if(sNota == Notas[i][0]):                              
            #time.sleep(wait_time)
            if(count_cicle == 0):
                player.note_on(Notas[i][1], volume)  #enciende la nota
                sNotaDet = Notas[i][0]
                print (sNotaDet)                  
                count_cicle +=1    
            elif(count_cicle <= wait_cicle):   
                cv2.putText(img, sNotaDet, (75,120), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX , 2, (0,255,0),6)     
                count_cicle +=1
            else:    
                player.note_off(Notas[i][1], volume)  #apaga la nota 
                sNota = ""
                count_cicle = 0            
            break

    if(count_cicle > wait_cicle):
        count_cicle = 0
        for i in range(len(Notas)):
            player.note_off(Notas[i][1], volume)  #apaga la nota 

def printValSet(valor):
    print("! se Cambio valo de seteo de prueba "+str(valor))

   
def calculateFingers(res,drawing):  # return finished bool, cnt: finger count
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 2:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):              
            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                             
                if  (angle <= math.pi / 2 ):  # math.pi / 2 (angle >= 0.7) and (angle <= 1.5): angle less than 90 degree, treat as fingers
                    cnt += 1
                    #dibuja circulo en el punto de defecto de convergencia interno
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1) 
                    # dibuja una linea que une los puntos externo OK
                    #cv2.line(drawing,start,end,(0,255,0),4)
                    #dibuja un ciculo en el punto externo de la mano
                    #cv2.circle(crop_img, end, 8, [100, 255, 255], -1)
                    cv2.circle(drawing, end, 8, [100, 255, 255], -1)
                    #escribe coordenadas sobre los dedos

                    if(modo_Debugge):
                        sAux = "["+str(end[0])+","+str(end[1])+"]"
                        cv2.putText(drawing, sAux, (end[0],end[1]-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255,255,255),1)
                   
            return True, cnt
    return False, 0



# initize Pygame MIDI ----------------------------------------------------------
pygame.midi.init()
# set the output device --------------------------------------------------------
player = pygame.midi.Output(device)
# set the instrument -----------------------------------------------------------
player.set_instrument(vInstrumento[instrumento][1])

bGuardar = True
cap = cv2.VideoCapture(0)
cap.set(10,200)


ret, img = cap.read()  #captura imagen de webcam
img = cv2.flip(img, 1) # rota la imagen espejada

cv2.rectangle(img, (0,int(img.shape[1]*0.3) ), (int(img.shape[0]*0.5),img.shape[1]), (255,0,0),2) #dibuja rectangulo de captura finder
aBor = 0 #ajusta el borde del contorno
crop_img = img[int(img.shape[1]*0.3)+aBor:img.shape[0]-aBor, aBor:int(img.shape[0]*0.5)-aBor] #recorta imagen a analizar para puntero

drawing = crop_img  #inicializa la imagen drawing

print("Music Finger Pointer V1.0 - 16-10.217 NeoRoboticTV")
print("[ESC] para salir [b] guarda fondo [d] modo desarrolador [i] cambia instrumento musical")

while cap.isOpened():
    ret, img = cap.read()
    img = cv2.flip(img, 1)

    # metodo 2 de definicion de zona de captura
    cv2.rectangle(img, (0,int(img.shape[1]*0.3) ), (int(img.shape[0]*0.5),img.shape[1]), (255,0,0),2)
    crop_img = img[int(img.shape[1]*0.3)+aBor:img.shape[0]-aBor, aBor:int(img.shape[0]*0.5)-aBor]

    if (bGuardar): #guarda la imagen de fondo        
        cv2.imwrite( 'fondo_box1.png',crop_img)
        bGuardar=False

    #lee el fondo de la imagen
    fondo_box1 = cv2.imread('fondo_box1.png') 
    
    #restamos la imagen con el fondo
    resta = cv2.subtract(fondo_box1,crop_img) #diferencia comun 
    #resta = cv2.absdiff (fondo_box1,crop_img) #diferencia absoluta 
    
    # filtro de desenfoque
    resta = cv2.blur(resta,(5,5)) 

    # convert to grayscale
    grey = cv2.cvtColor(resta, cv2.COLOR_BGR2GRAY)

    # applying gaussian blur
    value = (15, 15)
    blurred = cv2.GaussianBlur(grey, value, 0)

    # thresholdin: Otsu's Binarization method
    _, thresh1 = cv2.threshold(blurred, 35, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)  

    # check OpenCV version to avoid unpacking error
    (version, _, _) = cv2.__version__.split('.')

    if version == '3':
        _, contours, hierarchy = cv2.findContours(thresh1.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    elif version == '2':
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)
    
    # pinta botones
    pYo = aBor - 15
    pXo = int(img.shape[1]*0.3)+aBor
    pBtn = [ (40,110),(65,74),(90,40), (135,20), (180,40),(205,74),(230,110) ]
    for i in range(len(pBtn)):
         pXY =  pBtn[i]
         pCenter = ( pYo +  pXY[0] ,pXo + pXY[1] )
         cv2.circle(img, pCenter, 18, [0,0,255], 2)
         cv2.putText(img, str(i), (pCenter[0]-5,pCenter[1]+5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255),2)

         if(modo_Debugge):
                sAux = "["+str(pXY[0])+","+str(pXY[1])+"]"
                cv2.putText(img, sAux, (pCenter[0]-20,pCenter[1]-60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (0,255,255),1)
            
    # find contour with max area metodo 1
    #res = max(contours, key = lambda x: cv2.contourArea(x))
    
    # find contour with max area metodo 2
    length = len(contours)
    maxArea = -1
    count_defects = 0
     
    if length > 0:
        ci=0 
        for i in range(length):  # find the biggest contour (according to area)
            temp = contours[i]
            area = cv2.contourArea(temp)
            if area < 34000 and area > 20000 :
                if area > maxArea :
                    maxArea = area
                    ci = i
            #       print (ci)
            #print (area)
            res = contours[ci]

             # finding convex hull
            hull = cv2.convexHull(res)

            # dibuja los conteornos
            drawing = np.zeros(crop_img.shape,np.uint8)
            if(modo_Debugge):
                cv2.drawContours(drawing, [res], 0, (0, 255, 0), 0)
                cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 4)
   
            isFinishCal,count_defects = calculateFingers(res,drawing)
            
            #    busca el dedo indicador
            vPun =[1000,1000]
            for i in range(len(hull)):  # calculate the angle    
                Min = tuple(hull[i][0])                                
                if  (Min[1] < vPun[1] ):  
                    vPun = Min     

            if  (vPun[1]> 0 ):     
              
              if (vPun[1] < 200 ):   # no dibuja puntero por debajo de 200            
                cv2.circle(crop_img, vPun, 10, [255, 84, 0], -1) 
                if(modo_Debugge):
                    sAux = "["+str(vPun[0])+","+str(vPun[1])+"]"
                    if ( vPun[0] > 120):
                        cv2.putText(crop_img, sAux, (vPun[0]-100,vPun[1]-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0),1)
                    else:
                        cv2.putText(crop_img, sAux, (vPun[0]+10,vPun[1]-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0),1)

                #recorre y busca en cada punto del HULL
                for i in range(len(pBtn)):
                     btnX= pBtn[i][0] 
                     ptrX = vPun[0]
         
                     if (ptrX >= btnX - 30 )&(ptrX < btnX  ): # si esta dentro del area en X
                         btnY= pBtn[i][1] 
                         ptrY = vPun[1]                         
                         
                         if (ptrY >= btnY - 15 )&(ptrY < btnY + 15  ): # si esta dentro del area en y                            
                            #print ("detectado",vPun,pBtn[i])
                            pXY =  pBtn[i]
                            pCenter = ( pYo +  pXY[0] ,pXo + pXY[1] )
                            cv2.circle(img, pCenter, 18, [0,255,255], -1)
                            cv2.putText(img, str(i), (pCenter[0]-5,pCenter[1]+5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0),2)

                            #envia notas de acuerdo al i del vector boton en donde esta el finger pointer
                            if (i==0):
                                play_Nota("DO")
                            elif (i==1):
                                play_Nota("RE")
                            elif (i==2):
                                play_Nota("MI")
                            elif (i==3):
                                play_Nota("FA")
                            elif (i==4):
                                play_Nota("SOL")
                            elif (i==5):
                                play_Nota("LA")
                            elif (i==6):
                                play_Nota("SI")

    # show appropriate images in windows
    cv2.imshow('music finger pointer', img)

    if(modo_Debugge):
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)   
        cv2.imshow('Thresholded', thresh1)
        #cv2.imshow('Resta', resta)
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('crop_img', crop_img)
 
    k = cv2.waitKey(10)
    if k == 27:
        break
    elif k == ord('b'): #guarda imagen de fondo
        bGuardar = True
    elif k == ord('d'): #activa desactiva modo desarrollo debugge
        modo_Debugge = not modo_Debugge
        if (modo_Debugge): 
            print("ACTIVADO: Modo desarollador ")
        else:
            print("DESACTIVADO: Modo desarollador ")
            cv2.destroyWindow("Contours")
            cv2.destroyWindow("Thresholded")
    elif k == ord('i'): #cambia el instrumento       
        instrumento=instrumento+1  
        if(instrumento < (len(vInstrumento))):                                   
            player.set_instrument(vInstrumento[instrumento][1])
            print(instrumento,": ",vInstrumento[instrumento])
        else:
            instrumento = 0
            player.set_instrument(vInstrumento[instrumento][1])
            print(instrumento,": ",vInstrumento[instrumento])

del player
pygame.midi.quit()