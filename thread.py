from threading import Thread
import cv2

# Starting our class definintion
class ThreadCapture(Thread):
        """ Makes the video capture stream run in a seperate thread
            to the main part of the script """
        def __init__(self,):
                # ThreadCapture will become a child of the Thread Class through inheritance
                # this is so that we can overite the run() method of the Thread class to be what
                # we want to thread
                super(ThreadCapture, self).__init__()

                # Creates a video stream and initializes the variables we need to analyze the frames
                # (i.e. grabbed and frame). Stopped will be used to kill the thread when we press the
                # exit key
                self.stream = cv2.VideoCapture(0)
                (self.grabbed, self.frame) = self.stream.read()
                self.stopped = False

                self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


        # the run() method contains the process that will be put in the seprate thread.
        # In our case it is the pulling of the frames from the video capture that we want
        # to process.
        def run(self):
                while not self.stopped:
                        # This updates the instance variables "grabbed" and "frame" with the newest frame 
                        # from the stream.
                        (self.grabbed, self.frame) = self.stream.read()
                        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

                        faces = self.faceCascade.detectMultiScale(gray, 5, minNeighbors=1)

                        # Draw a rectangle around the faces
                        for (x, y, w, h) in faces:
                                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                roi_gray = gray[y:y+h, x:x+w]
                                roi_color = self.frame[y:y+h, x:x+w]
                else:
                        self.stream.release()

        # Allows us to access the frame variables that are contained in the thread                      
        def getFrame(self):
                return self.frame

        # Will stop the video capture by ending the loop in the thread  
        def stop(self):
                self.stopped = True


# Now we are back in the main part of the script where we will process the frames
# Loading the face cascade
"""faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')"""

# Creates a an instance of the ThreadCapture class that we created              
thread1 = ThreadCapture()
thread1.setDaemon(True)
print thread1.isDaemon()

# Start is a method of the Thread class. It activates the threading of the run() method 
thread1.start()

# This loop will display the frames
while True:
        #fram = thread1.getFrame()

        """# Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]"""

        cv2.imshow('Frame', thread1.getFrame())
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Clean up
thread1.stop()
cv2.destroyAllWindows()
print thread1.isAlive()
                
