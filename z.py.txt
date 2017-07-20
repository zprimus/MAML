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
        self.end = False
        self.frame_count = 0
        self.rangecount = 0
        self.increase = True
        self.decrease = False
        self.x_set = False
        self.y_set = False
 #       self.smile = False
        self.dcx = 4.5
        self.dcy = 3

        self.x_plus = False
        self.x_minus = False
        self.y_plus = False
        self.y_minus = False

    """ This is the method that is threaded in the background. It is originally from the Thread
        class, but we are rewriting so that it threads what we desire"""
    def run(self): #pass the method the angles we want the servo to start at

        self.pwmy.start(self.dcy)      #starts at the angle we specify  

        self.pwmx.start(self.dcx) 

        while True:
            if self.end == True:
                break

            if self.stopped:
                if (not self.x_set):
                    self.movex()
                    sleep(.75)
                    continue
                if (not self.y_set):   
                    self.movey()
                    sleep(.75)
                    continue
                else:
                    self.fire()
                    
            else: # These statements will cause the camera to sweep
                if self.increase:
                    self.dcx += .25
                    self.pwmx.ChangeDutyCycle(self.dcx)
                    if self.dcx >= 9:
                        self.increase = False
                        self.decrease = True
                    sleep(1)
                    continue
                if self.decrease:
                    self.dcx -= .25
                    self.pwmx.ChangeDutyCycle(self.dcx)
                    if self.dcx < 4.5:
                        self.increase = True
                        self.decrease = False
                    sleep(1)
                    continue

    def getDcx(self):
            return self.dcx

    def getDcy(self):
            return self.dcy    

    # x and y are references to place in image determined by pixels
    # desiredAngles are refernces to the current angle that the servos are at
    # get x,y from fast and angles from servox/sweep
    
    def movex(self):

   #     print("x: %d" %x)
     #   print("y: %d" %y)
        
        if (self.x_minus):
            self.dcx -= .1
      #      print("%d" % self.dcx)
            self.pwmx.ChangeDutyCycle(self.dcx)
    #        print("x-")
            return

        elif (self.x_plus): 
            self.dcx += .1
     #       print("%d" % self.dcx)
            self.pwmx.ChangeDutyCycle(self.dcx)
    #        print("x+")
            return
        else:
            self.x_set = True


    def movey(self):
    #    print("x: %d" %x)
   #     print("y: %d" %y)
        
        if (self.y_minus):
            self.dcy -= .1
     #       print("%d" % self.dcy)
            self.pwmy.ChangeDutyCycle(self.dcy)
    #        print("y-")
            return
        
        elif (self.y_plus):
            self.dcy += .1
            self.pwmy.ChangeDutyCycle(self.dcy)
     #       print("y+")
            return
        
        else:
            self.y_set = True

           
    def fire(self):        
          print("RANGE")

          self.pwmy.ChangeDutyCycle(self.dcy + 2.5)
          sleep(1)
          GPIO.output(self.sole,GPIO.HIGH)
          sleep(2)
          GPIO.output(self.sole,GPIO.LOW)
          self.pwmy.ChangeDutyCycle(7);
          sleep(12.5)
          self.pwmy.ChangeDutyCycle(2.5);
          self.stopped = False # Once we fire we will start sweeping again
          self.x_set = False
          self.y_set = False



# end class def


# Start main thread
# Load cascades
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

cap = cv2.VideoCapture(0)
cap.set(3,300)
cap.set(4,300)
cap.set(5,40)

serv = ThreadServo()

serv.start()
        
while True:
    # Capture frame-by-frame
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.15,        #for distance, decrease 
        minNeighbors=3,
        )

    for (x, y, w, h) in faces:
        
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) 
        
        '''roi_gray = gray[y:y+h, x:x+w]
     #   roi_color = img[y+h/2:y+h, x:x+w]
        
        smiles = smile_cascade.detectMultiScale(
                roi_gray,
                )
        for (ex,ey,ew,eh) in smiles:
             #   pass
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)'''

    
        
    if np.any(faces):
        serv.frame_count = 0
        serv.stopped = True        
        '''if np.any(smiles):
            serv.smile = True
        else:
            serv.smile = False'''
        if x > 160:
            serv.x_plus = False
            serv.x_minus = True
        elif x < 140:
            serv.x_plus = True
            serv.x_minus = False
        elif x > 140 and x < 160:
            serv.x_plus = False
            serv.x_minus = False

        if y > 160:
            serv.y_plus = False
            serv.y_minus = True
        elif y < 140:
            serv.y_plus = True
            serv.y_minus = False
        elif y > 140 and y < 160:
            serv.y_plus = False
            serv.y_minus = False

        """if x >110 and x < 140:
            serv.xset = True
        
        if serv.xset is False:
            serv.movex(x + w/2, serv.getDcx())
            sleep(1)
        else:
            if serv.movey(y + h/2, serv.getDcy()) is True:
                serv.rangecount += 1
                if serv.rangecount == 3:
                    serv.fire()
        """
    elif (serv.stopped):
  #      if (serv.stopped == True): # if we have stopped the sweep we will
        serv.frame_count += 1
        print ("%d" %serv.frame_count)
        if (serv.frame_count == 45):
            serv.pwmy.ChangeDutyCycle(2.5);
            serv.stopped = False
            
            serv.frame_count = 0

               
    cv2.imshow('image', img)
    
    k=cv2.waitKey(30) & 0xff
    if k == 27:
        serv.stopped = True
        break
    
cap.release()
cv2.destroyAllWindows()
serv.end = True
serv.pwmx.stop
serv.pwmy.stop
GPIO.cleanup()

#print self.dcx

#mess with scalefactor and resolution to find which increases cpu power usage more
#keep fps at a minimum
#what could possibly make the servos go into undefined behavior (Power? code? CPU power)?

# Need to have pinpoint adjust on a frame per frame basis instead
# of in a while loop so we can have the frames still displayeed
