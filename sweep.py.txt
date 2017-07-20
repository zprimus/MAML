import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
servoPinx=11
GPIO.setup(servoPinx, GPIO.OUT)
pwm=GPIO.PWM(servoPinx,50)

pwm.start(6.525) #starts in the middle
desiredAngle = 90

while(desiredAngle < 180):      #gradually turns counterclockwise by diminishing the change duty cycle
        desiredAngle += 4.5             
        DC=8.75/180.*(desiredAngle)+2
        pwm.ChangeDutyCycle(DC)         
        sleep(.25)
        if (desiredAngle == 180):               #first while loop control flows to second when servo is rotated to 180 degrees
                while(desiredAngle > 0):        #gradually turns clockwise by increasing the change duty cycle
                        desiredAngle -= 4.5
                        DC=8.75/180.*(desiredAngle)+2
                        pwm.ChangeDutyCycle(DC)
                        sleep(.25)
                        if(desiredAngle == 0):  #second while loop terminates when servo is rotated to 0 degrees
                                sleep(.25)
                                break
	
pwm.stop()                                      #Servo stops rotating... unreachable code                 
GPIO.cleanup()
	

