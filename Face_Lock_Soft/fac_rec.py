
import cv2
import numpy as np
from PIL import Image
import os
import pickle
import sys
import time


def main():

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    cascadePath = "face.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    counts =[]
    timerlocked = False
    ref_time =0
    cur_time =0
    #iniciate id counter
    id = 0
    try:
        names=pickle.load(open("names.dat","rb"))
        recognizer.read('trainer/trainer.yml')

    except FileNotFoundError:
        names=[]
        print ("Name and Trainer file is not present, Terminating program...\n\n")	
        for i in range(27):
            print('-> ',end='')
            time.sleep(0.1)
        sys.exit()
        



    # names related to ids: example ==> Ram: id=1,  etc
    #names = ['None', 'Ram', 'sam','Akshatha','Adarsh'] 

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    # Define min window size to be recognized as a face

    while True:

        ret, img =cam.read()
        
        img = cv2.flip( img, 1 )# Flip Horrizontally
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x,y,w,h) in faces:
            label, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    
          
            # Check if confidence is less than 100 ==> "0" is perfect match 
            if (confidence < 80 ):
                name = names[label]
                confidence = "  {0}".format(round(100 - confidence))
            else:
                name = "unknown"
                cv2.imwrite("Unknowns/un.jpg",gray[y:y+h,x:x+w])
                confidence = "  {0}".format(round(100 - confidence))
            
            cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,0,255), 2)
            cv2.putText(img, str(confidence)+"%", (x+5,y+h-5), font, 1, (0,0,25), 2)    
                

            if name in names:

                if not timerlocked:
                    ref_time = time.ctime()[17] + time.ctime()[18]
                    timerlocked = True
                    print("New ref_time = ",ref_time)

                if int(confidence) > 65:
                    cv2.putText(img, "Unlocking..Hold still  " + str(3 - (cur_time - int(ref_time)) ), (x-40,y-60), font, 1, (0,255,0), 2)
                else:
                    cv2.putText(img, "Locked", (x+5+w,y+h-5), font, 1, (0,0,255), 2)
                    print("Face not matched ....Reseting timer ")
                    print("cur_TIME",cur_time)
                    timerlocked = False
                    
                    

                cur_time = int(time.ctime()[17] + time.ctime()[18])
                print("curtime =",cur_time)
                if (cur_time - int(ref_time))== 3 : 
                    cv2.destroyAllWindows()
                    cam.release()
                    sys.exit()
                elif (cur_time - int(ref_time)) > 3 : 
                    timerlocked = False  
            else:
                print("not matched")
                


                    
        cv2.imshow('camera',img) 
             
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
