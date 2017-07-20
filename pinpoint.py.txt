import RPi.GPIO as GPIO

class servo():                                                  #class defines all servo functions

        def __init__():
        
                GPIO.setmode(GPIO.BOARD)
                servoPinx=11
                servoPiny=12
                GPIO.setup(servoPinx, GPIO.OUT)
                GPIO.setup(servoPiny, GPIO.OUT)

                pwmx=GPIO.PWM(servoPinx,50)
                pwmy=GPIO.PWM(servoPiny,50)

                pwmx.start(6.525) #starts in the middle
                pwmy.start(2.486)

# x and y are references to place in image determined by pixels
# desiredAngles are refernces to the current angle that the servos are at
# get x,y from fast and angles from servox/sweep

        def move(x, y, desiredAnglex, desiredAngley):           #rotates the x and y axis servos to the requested angle

                if ( x > 260 ): esiredAnglex = x - 2

                if ( x < 240 ): desiredAnglex = x + 2
                
                if ( y > 260 ): desiredAngley = y - 2

                if ( y < 240 ): desiredAngley = y + 2
 

                Dx=8.75/180.*(desiredAnglex)+2                  # determines the x-axis servo Magnetic field magnitude to be generated
                pwmx.ChangeDutyCycle(Dx)                        # Magnetic field Magnitude is generated to move x-axis servo to desired location
                Dy=8.75/180.*(desiredAngley)+2                  # determines the y-axis servo Magnetic field magnitude to be generated
                pwmy.ChangeDutyCycle(Dy)                        # Magnetic field Magnitude is generated to move y-axis servo to desired location

                pwmx.stop()                                     #Magnetic field is terminated for X and Y servos
                pwmy.stop()
                GPIO.cleanup()
