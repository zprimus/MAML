from threading import Thread
from time import sleep
import numpy as np
import cv2
import RPi.GPIO as GPIO
#import pinpoint

class ThreadServo (Thread):

    def __init__(self):
        super(ThreadServo, self).__init__()
        # Set up the pins on the pi
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.servoPinx=15
        self.servoPiny=16
        self.sole = 22
        GPIO.setup(self.servoPinx, GPIO.OUT)
        GPIO.setup(self.servoPiny, GPIO.OUT)
        GPIO.setup(self.sole, GPIO.OUT)

        self.pwmx=GPIO.PWM(self.servoPinx,50)
        self.pwmy=GPIO.PWM(self.servoPiny,50)
        self.pwms=GPIO.PWM(self.sole,50)

        # Variables that will control the run method
        self.stopped = False
        self._break = False
        self.movestop = False
        self.frame_count = 0
        self.increase = True
        self.decrease = False
        self.dcx = 4.5
        self.dcy = 3.5

    """ This is the method that is threaded in the background. It is originally from the Thread
        class, but we are rewriting so that it threads what we desire"""
    def run(self): #pass the method the angles we want the servo to start at

        serv.pwmy.start(serv.dcy)      #starts at the angle we specify  

        serv.pwmx.start(serv.dcx) 

        while True:
            if self._break == True:
                break
            if self.stopped:
                pass
            else: # These statements will cause the camera to sweep
                if self.increase:
                    self.dcx += .5
                    self.pwmx.ChangeDutyCycle(self.dcx)
                    if self.dcx >= 9:
                        self.increase = False
                        self.decrease = True
                    sleep(.5)
                    continue
                if self.decrease:
                    self.dcx -= .5
                    self.pwmx.ChangeDutyCycle(self.dcx)
                    if self.dcx < 4.5:
                        self.increase = True
                        self.decrease = False
                    sleep(.5)
                    continue

    def getDcx(self):
            return self.dcx

    def getDcy(self):
            return self.dcy    

    def move(self, x, y, anglex, angley):

    # x and y are references to place in image determined by pixels
    # desiredAngles are refernces to the current angle that the servos are at
    # get x,y from fast and angles from servox/sweep

        print("x: %d" %x)
        print("y: %d" %y)

        
        if (x > 140):
            self.dcx = anglex - .5
            self.pwmx.ChangeDutyCycle(self.dcx)
            print("x-")
            #return

        elif ( x < 110): 
            self.dcx = anglex + .5
            self.pwmx.ChangeDutyCycle(self.dcx)
            print("x+")
            #return            

        if (x < 140 and x > 110): # will kill the x servo once it is in range
            self.pwmx.stop
            
            if (y > 140):
                self.dcy = angley - .5  
                self.pwmy.ChangeDutyCycle(self.dcy)
                print("y-")
                #return 
                
            elif (y < 110):
                self.dcy = angley + .5
                self.pwmy.ChangeDutyCycle(self.dcy)
                print("y+")
                #return
            
        if( (x < 140 and x > 110) and (y > 110 and y < 140)):
              self.movestop = True
              print("RANGE")
              self.pwmy.ChangeDutyCycle(self.dcy + .5)
              sleep(1)
              GPIO.output(self.sole,GPIO.HIGH)
              sleep(1)
              GPIO.output(self.sole,GPIO.LOW)
              self.pwmy.ChangeDutyCycle(self.dcy);
              self.stopped = False # Once we fire we will start sweeping again


# End Class def


# Load cascades
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

cap = cv2.VideoCapture(0)
cap.set(3,250)
cap.set(4,250)
cap.set(5,30)

serv = ThreadServo()

serv.start()
        
while True:
    # Capture frame-by-frame
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,        #for distance, decrease 
        minNeighbors=4,
        )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) 
        
        roi_gray = gray[y+h/3:y+h, x:x+w]
        roi_color = img[y+h/3:y+h, x:x+w]
        
        """smiles = smile_cascade.detectMultiScale(
            roi_gray,
            )
        
        for (ex,ey,ew,eh) in smiles:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            break"""

    if np.any(faces):
       # print("true")
        serv.frame_count = 0
        serv.stopped = True
        
        if (not serv.movestop):
            serv.move(x + w/2, y + h/2, serv.getDcx(), serv.getDcy()) 
    else:
        #print("false")

        if (serv.stopped == True): # if we have stopped the sweep we will
            serv.frame_count += 1
           # print ("%d" % serv.frame_count)
            if (serv.frame_count == 10):
                serv.pwmy.ChangeDutyCycle(3.5);
                serv.stopped = False
                serv.frame_count = 0

    cv2.imshow('image', img)
    
    k=cv2.waitKey(30) & 0xff
    if k == 27:
        serv.stopped = True
        break
    
cap.release()
cv2.destroyAllWindows()
serv._break = True
serv.pwmx.stop
serv.pwmy.stop
GPIO.cleanup()

#print self.dcx

#mess with scalefactor and resolution to find which increases cpu power usage more
#keep fps at a minimum
#what could possibly make the servos go into undefined behavior (Power? code? CPU power)?

# Need to have pinpoint adjust on a frame per frame basis instead
# of in a while loop so we can have the frames still displayeed
