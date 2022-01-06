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
import datetime

from smbus2 import SMBus
from mlx90614 import MLX90614
bus = SMBus(1)

from Adafruit_CharLCD import Adafruit_CharLCD

sensor = MLX90614(bus, address=0x5A)

#relay
relay = 12

#LED
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)

# LCD Pins
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()

#connect to database
mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing" 
    )
cursorA = mydb.cursor(buffered=True)


def getProfile(ID):
    cmd="SELECT * FROM test WHERE pID+" + str(ID)
    cursorA.execute(cmd)
    profile = None
    for row in cursorA:
        profile=row
    mydb.commit()
    #cursorA.close()
    return profile


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay ,1)

#camera resolution
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = (640, 480))

recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer.read('trainer.yml')
font = cv2.FONT_HERSHEY_SIMPLEX
dtime = datetime.datetime.now()

##### w/o sql database #####
#id counter
#id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
#names = ['Lala', 'Milky', 'Covid']

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port = True):
    frame = frame.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors =5)
    
    for (x,y,w,h) in faces :
        roiGray = gray[y:y+h, x:x+w]
        
        id_, conf = recognizer.predict(roiGray)
        profile=getProfile(id_)
        if profile!=None and conf <= 95:
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(20,GPIO.LOW)
            conf = "{0}%".format(round(100-conf))
            GPIO.output(relay, 0)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, str(profile[2])+ str(conf), (x,y), font, 2, (0,0,255), 2, cv2.LINE_AA)
            time.sleep(5)
            GPIO.output(relay, 1)
            print(dtime)
            lcd.message('Welcome ' + str(profile[2]))
            #time.sleep(7)
            
            
        else:
            GPIO.output(relay, 1)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(20,GPIO.HIGH)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Unknown", (x,y), font, 2, (0,0,255), 2, cv2.LINE_AA)
            #camera.capture('facedb/strangers/intruder.jpg')
            
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    
    rawCapture.truncate(0)
    
    if key == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cv2.destroyAllWindows()