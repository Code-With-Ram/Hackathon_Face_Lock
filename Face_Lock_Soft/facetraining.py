
import cv2
import numpy as np
from PIL import Image
import os
import sys

def main():
    # Path for face image database
    Path = 'FaceSamples'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("face.xml");


    def getImagesAndLabels(Path):

        imagePaths = [os.path.join(Path,f) for f in os.listdir(Path)]     
        		
        

            
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:
            
            gray_img = Image.open(imagePath).convert('L') # convert it to grayscale

            img_numpy = np.array(gray_img,'uint8')
            label = int(os.path.split(imagePath)[1].split(".")[0].replace("face-", " "))
            print(label)
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(label)
                cv2.imshow("Training ",img_numpy)
                cv2.waitKey(12)
        return faceSamples,ids


    print ("\n INFO---> Training faces. It will take a few seconds. Wait ...")
    faces,ids = getImagesAndLabels(Path)
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.save('trainer/trainer.yml')  
    #print(ids)
    # Print the numer of faces trained and end program
    print("\n INFO---> {0} faces trained. Exiting Program".format(len(np.unique(ids))))




    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
