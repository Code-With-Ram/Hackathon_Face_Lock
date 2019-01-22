import cv2
import os
import pickle
import time
import sys

def main():
    cam = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier('face.xml')

    # For each person, enter one numeric face id

    offset=50

    print("\n INFO---> Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0
    try:
        id_list=pickle.load(open("id_list.dat","rb"))
        print(id_list)
        Id = len(id_list)
        print(Id)
    except FileNotFoundError:
        print ("Name file is not present, skipping the reading process...")	
	
	
    while(True):
        
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces=face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)

        for (x,y,w,h) in faces:

            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("FaceSamples/face-" + str(Id) + '.' + str(count) + ".jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])

            cv2.rectangle(img, (x-50,y-50), (x+w+50,y+h+50), (225,0,0), 2)     

            cv2.imshow('image', img)

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 25: # Take  face sample and stop video
             break

    # Do a bit of cleanup
    print("\n INFO---> Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
