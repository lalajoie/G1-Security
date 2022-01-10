############################ LIBRARIES ############################
from __future__ import print_function
import cv2
import os
import os.path
import mysql.connector
import datetime
import time
import numpy as np
import numpy as n
import RPi.GPIO as GPIO
import pickle
import multiprocessing
import smtplib
import telerivet
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from smbus2 import SMBus
from mlx90614 import MLX90614

############################ MODULES ############################

#LCD
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)

#Relay
relay = 12

#LED
white = 21
red = 20

#Ultrasonic
GPIO_TRIGGER = 18
GPIO_ECHO = 23


#################################################################

mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing" 
    )
cursorA = mydb.cursor(buffered=True)

#################################################################

# def createDataset():
#     cam = cv2.VideoCapture(0)
#     cam.set(3, 640) # set video width
#     cam.set(4, 480) # set video height
#     face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     #id name and input
#     face_id = input('Enter User ID: ')
#     face_name = input('Enter Name:')
#     lcd.message('Hello ' + str(face_name))
#     time.sleep(2)
#     lcd.clear()
#     dtime = datetime.datetime.now()
#     print("\n [INFO] Initializing face capture. Look the camera and wait ...")
#     lcd.message('Look at the \n camera and wait')

#     facesql = "INSERT INTO test (userID, userName, timeDate) VALUES (%s, %s, %s)"
#     faceval = (face_id, face_name, dtime)
#     cursorA.execute(facesql, faceval)
#     mydb.commit() 

#     count = 0
#     while(True):
#         ret, frame = cam.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_detector.detectMultiScale(gray, 1.3, 5)
#         for (x,y,w,h) in faces:
#             cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)     
#             count += 1
#             # Save the captured image into the folder
#             cv2.imwrite("facedb/" + str(face_name) + '.' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
#             cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)	

#             cv2.imshow('image', frame)
#         k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
#         if k == 27:
#             break
#         elif count >= 50: # Take 50 face samples and stop video
#             break

#     lcd.clear()

#     print("\n [INFO] Exiting Program and cleanup stuff")
#     lcd.message('Face Registered')

#     cam.release()
#     cv2.destroyAllWindows()

#################################################################

# def trainer():
#     path = 'facedb/'

#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     # function to get the images and label data
#     def getImagesAndLabels(path):
#         imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
#         faceSamples=[]
#         ids = []
#         for imagePath in imagePaths:
#             PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
#             img_numpy = np.array(PIL_img,'uint8')
#             id = int(os.path.split(imagePath)[-1].split(".")[1])
#             faces = detector.detectMultiScale(img_numpy)
#             for (x,y,w,h) in faces:
#                 faceSamples.append(img_numpy[y:y+h,x:x+w])
#                 ids.append(id)
#         return faceSamples,ids

#     lcd.message('Training faces \nPlease wait..')
#     print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")

#     faces,ids = getImagesAndLabels(path)
#     recognizer.train(faces, np.array(ids))

#     # Save the model into trainer/trainer.yml
#     recognizer.write('trainer.yml') 

#     # Print the numer of faces trained and end program
#     lcd.clear()
#     lcd.message("{0} faces trained \nExiting Program".format(len(np.unique(ids))))
#     print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

#################################################################
def recognize():
    GPIO.setup(white,GPIO.OUT)
    GPIO.setup(red,GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay, GPIO.OUT)
    GPIO.output(relay ,1)
    
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size = (640, 480))
    
    def getProfile(ID):
        cmd="SELECT * FROM test WHERE pID+" + str(ID)
        cursorA.execute(cmd)
        profile = None
        for row in cursorA:
            profile=row
        mydb.commit()
        #cursorA.close()
        return profile

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    recognizer.read('trainer.yml')
    font = cv2.FONT_HERSHEY_SIMPLEX
    dtime = datetime.datetime.now()
    lcd.clear()
    lcd.message("recognizer on")
        
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port = True):
        frame = frame.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors =5)
        
        for (x,y,w,h) in faces :
            roiGray = gray[y:y+h, x:x+w]
            
            id_, conf = recognizer.predict(roiGray)
            profile=getProfile(id_)
            if profile!=None and conf <= 95:
                lcd.clear()
                lcd.message('Welcome, \nScan Temp')
                gettemp()
                print("ok")
                #GPIO.output(relay, 0)
                GPIO.output(21,GPIO.HIGH)
                GPIO.output(20,GPIO.LOW)
                conf = "{0}%".format(round(100-conf))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, str(profile[2])+ str(conf), (x,y), font, 2, (0,0,255), 2, cv2.LINE_AA)
                gettemp()
                time.sleep(10)
                #GPIO.output(relay, 1)
                #print(dtime)
                #time.sleep(7)
                #time.sleep(5)
                #break
                
            else:
                lcd.clear()
                lcd.message("unknown face")
                GPIO.output(relay, 1)
                GPIO.output(21,GPIO.LOW)
                GPIO.output(20,GPIO.HIGH)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Unknown", (x,y), font, 2, (0,0,255), 2, cv2.LINE_AA)
                camera.capture('strangers/intruder.jpg')
                sendemail()
                txtmsg()
                
                
        #camera.close()
        #ultrasonic()
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        
        rawCapture.truncate(0)
        
        if key == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cv2.destroyAllWindows()

#################################################################

def sendemail():
    fromaddr = "g1sec.notif@gmail.com"
    toaddr = "lalajoiedg@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "g1Sec - SOMEONE'S AT YOUR DOOR"
    body = 'There is a stranger at your door.'
    msg.attach(MIMEText(body, 'plain'))

    filename = "intruder.jpg"
    attachment = open("/var/www/html/g1-Security/python/strangers/intruder.jpg", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= {}".format(filename))
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "g1secthesis")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    time.sleep(20)

#################################################################

def txtmsg():
    API_KEY = '6vi3m_1fY1hW5N5wlJowBiYC3xHd68ex8S6m'  # from https://telerivet.com/api/keys
    PROJECT_ID = 'PJac1b0ccab951ab23'

    tr = telerivet.API(API_KEY)

    project = tr.initProjectById(PROJECT_ID)

    # Send a SMS message
    project.sendMessage(
        to_number = '+639217301559',
        content = 'Unknown person detected. Check your email to see the unidentified person. \n\n\nFrom G1 Security'
    )
    lcd.clear()
    lcd.message('message sent')


#################################################################

def gettemp():
    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)
    time.sleep(15)
    print ("Ambient Temperature :", sensor.get_ambient())
    print ("Object Temperature :", sensor.get_object_1())
    obj = sensor.get_object_1()
    strob = str(obj)
    lcd.clear()
    lcd.message('Temp: ' + strob)
    bus.close()
    
    

#################################################################

def ultrasonic():
    
    GPIO.setmode(GPIO.BCM)
    
    #set GPIO Pins
    GPIO_TRIGGER = 18
    GPIO_ECHO = 23
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
    def distance():
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
    
    if __name__ == '__main__':
        try:
            while True:
                dist = distance()
                print ("Measured Distance = %.1f cm" % dist)
                time.sleep(1)
                if dist <= 30:
                    p = multiprocessing.Process(target = recognize, name = "reco")
                    p.start()
                    time.sleep(60)
                    p.terminate()
                    p.join()
    
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()

#################################################################

if __name__ == '__main__':
    lcd.clear()
    ultrasonic()
