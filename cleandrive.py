'''CLEANDRIVE - AN ALCOHOL DRUNK AND DRIVE ACCIDENT PREVENTION SYSTEM PROJECT

BY :
    VISHNU SANTHOSH
    G.ADARSH
    RAHUL P.R.
MENTOR :
    PROF.SIMI M.S.
'''

import time
import numpy as np
import cv2
import tkinter
from tkinter import Tk,mainloop,TOP
from tkinter.messagebox import _show
from tkinter.ttk import Button
import wiringpi as wiringpi
wiringpi.wiringPiSetupGpio()
from time import sleep
wiringpi.pinMode(23, 0) #GPIO Pin for Seatbelt(Physical Pin : 16)
wiringpi.pinMode(25,0) #GPIO Pin for MQ3 Alcohol Sensor(Physical Pin : 22)


# Seatbelt Initial Check
def seatbeltInit():
    print("\n\n ||  PLEASE INSERT YOUR SEATBELT  || ")
    sleep(1)
    lock=wiringpi.digitalRead(23)
    count=0
    duration=0
    while(duration<3):
        lock=wiringpi.digitalRead(23)
        if(lock==0):
            duration=0
            if(count==0):
                print("\n\nStatus : You haven't inserted your seatbelt\n")
            count+=1
            if(count>10):
                print("\n\nStatus : Seatbelt not inserted ! Try Again")
                exit(0)
        else:
            if(duration==0):
                print("\n\nStatus : Seatbelt Inserted. Please Wait !\n")
                count=0
            duration+=1
        sleep(2)
    print("\n\nSeatbelt confirmed !\n")
    sleep(2)

#Seatbelt Check
def seatbeltCheck():
    lock=wiringpi.digitalRead(23)
    return str(lock)

#Initialising Display function
def InitialisingMsg():
    root=Tk()
    root.title("Cleandrive")
    root.geometry('400x400+300+250')
    button = Button(root,text='Initialising . .')
    button.pack(side = TOP, pady=5)
    root.after(5000,root.destroy)
    mainloop()

#Facedetection along with Alcohol Testing
def FacedetectInit():
    #Facedetection using haarcascades classifier: https://github.com/Itseez/opencv/tree/master/data/haarcascades
    #Classifier path : CLEANDRIVE/Cascades/haarcascade_frontalface_default.xml
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    single_face_count=0
    multi_face_count=0
    no_face_count=0
    test_count=0
    status=0
    cheat=0
    test_lock=0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(20, 20))
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        cv2.imshow('video',img)
        if(len(faces) == 0): 
           if(no_face_count==6):
               print("\n\nStatus : No driver found. Register face data !\n")
               test_lock=1
           no_face_count+=1
           if(no_face_count>15):
               print("\n\n Status : No driver found. Try again")
               break
        else:
            if(str(faces.shape[0])=='1'):
                if(test_lock==1):
                    test_lock=0
                    single_face_count=0
                    test_count=0
                    no_face_count=0
                if(single_face_count==0):
                    print("\n\n Status : Registering Face Data. Please Wait !\n")
                single_face_count+=1
                if(seatbeltCheck()=='1'):
                    cheat=0
                    if(single_face_count>10):
                        if(test_count==0):
                            print("\n\n Status : Face Data Registered. Standby for Alcohol Testing  ")
                            sleep(1)
                        test_count+=1
                        if(test_count<15):
                            my_input=wiringpi.digitalRead(25)
                            if(my_input):
                                if(status==0):
                                    print("\n\n ALCOHOL TESTING STATUS: Not Detected. Please Wait !")
                                    
                                status+=1
                            else:
                                if(status!=0):
                                    print("\n\n Status : Alcohol Detected. Please Wait !")
                                status=0
                        else:
                            if(status>12):
                                sleep(1)
                                print("\n\n Status : Test passed ! Start the Engine")
                                sleep(1)
                                print("\n\n    * * * * H A V E  A  S A F E  J O U R N E Y :) * * * * ")
                                exit(0)
                            else:
                                sleep(1)
                                print("\n\n Status : You are Drunk ! Cannot start the engine\n\n  ")
                                exit(0)
                        sleep(0.4)
                else:
                    while(seatbeltCheck()!='1'):
                        if(cheat==0):
                            print("\n\n Status : You haven't inserted your seatbelt\n")
                        cheat+=1
                        
            elif(int(faces.shape[0])>1):
                if(multi_face_count==0):
                    print(" Detecting Multiple Faces ! Please register with one person infront of the camera.")
                multi_face_count+=1
                if(multi_face_count>5):
                    single_face_count=0
                    print(" Multiple  faces detected. Cannot Start the Engine ! \n\n")
                    exit(0)
                            
                
                
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
    
    
    
if __name__== "__main__":
#Stage 1
    print("\n\n     << CLEANDRIVE >>")
    sleep(2)
    print("\n\n  Calibrating . . Please Wait !")
    sleep(2)
    seatbeltInit()    
    print("\n\n **** Beginning Face Detection and Alcohol Testing **** \n")
#Stage 2
    InitialisingMsg()
    FacedetectInit()  
    


        

    

        
    
        
