import numpy as np
#import servo
#import sweep
import cv2

# Load cascades
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

#servo = servoxy

cap = cv2.VideoCapture(0)
cap.set(3,500)
cap.set(4,500)

detected = False

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #sets image to grayscale

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=2,        #for distance, decrease 
        minNeighbors=5,
        )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)  #displays a rectangle around any detected faces
        detected = True

        roi_gray = gray[y+h/3:y+h, x:x+w]
        roi_color = img[y+h/3:y+h, x:x+w]
        
        smiles = smile_cascade.detectMultiScale(                #detects smiles in image
            roi_gray,
            )
        
        for (ex,ey,ew,eh) in smiles:                            #displays a rectangle around any detected smiles
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            break
    

    cv2.imshow('image', img)                                    #feeds the rectangle layer to the colored picture
    
    k=cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
