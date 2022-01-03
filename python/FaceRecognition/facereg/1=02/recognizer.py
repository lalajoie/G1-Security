import cv2
import mysql.connector
import numpy as n
from picamera.array import PiRGBArray
from picamera import PiCamera
import os
import RPi.GPIO as GPIO
import pickle
import time
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD

# instantiate lcd and specify pins
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()

mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing" 
    )



#if (mydb.is_connected()):
#    print("Connected")
#else:
#    print("Not connected")

#mycursor = mydb.cursor()
cursorA = mydb.cursor(buffered=True)


def getProfile(ID):
    cmd="SELECT * FROM testingLogs WHERE ID+" + str(ID)
    cursorA.execute(cmd)
    profile = None
    for row in cursorA:
        profile=row
    mydb.commit()
    #cursorA.close()
    return profile

relay = 12

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay ,1)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = (640, 480))

recognizer = cv2.face.LBPHFaceRecognizer_create()

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

recognizer.read('trainer.yml')

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['Lala', 'Milky', 'Covid']

# Initialize and start realtime video capture
#cam = cv2.VideoCapture(0)
#cam.set(3, 320) # set video widht
#cam.set(4, 240) # set video height

# Define min window size to be recognized as a face
#minW = 0.1*cam.get(3)
#minH = 0.1*cam.get(4)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port = True):
    frame = frame.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors =5)
    
    
    for (x,y,w,h) in faces :
        roiGray = gray[y:y+h, x:x+w]
        
        id_, conf = recognizer.predict(roiGray)
        profile=getProfile(id_)
        
        if profile!=None and conf < 100:
            conf = "{0}%".format(round(100-conf))
            #GPIO.output(relay, 0)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, str(profile[1])+ str(conf), (x,y), font, 2, (0,0,255), 2, cv2.LINE_AA)
            lcd.message('Welcome ' + str(profile[1]))
            #time.sleep(5)
            #GPIO.output(relay, 1)
        else:
            #GPIO.output(relay, 1)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Unknown", (x,y), font, 2, (0,0,255), 2, cv2.LINE_AA)
            
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    
    rawCapture.truncate(0)
    
    if key == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cv2.destroyAllWindows()