import cv2
import os
import os.path
import mysql.connector
import datetime
import time
from time import sleep

from Adafruit_CharLCD import Adafruit_CharLCD #LCD Library


# LCD pins
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()

# connect to database
mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing" 
    )
mycursor = mydb.cursor(buffered=True)

#set camera width and height
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#def insertOrUpdate(ID,Name):
 #   cmd = "SELECT * FROM testingLogs"
  #  cursorA.execute(cmd)
   # isRecordExist = 0
   # for row in cursorA:
     #   isRecordExist = 1
     #   if (isRecordExist==1):
     #       cmd="UPDATE testingLogs SET Name= "+str(face_id)+"WHERE ID = " + str(face_id)
     #   else:
     #       cmd="INSERT INTO testingLogs(ID,Name) Values("+str(face_id)+","+str(face_name)+")"
     #       cursorA.execute(cmd)
     #      mydb.commit()
            
# id and name input
face_id = input('Enter User ID: ')
face_name = input('Enter Name:')
lcd.message('Hello ' + str(face_name))
time.sleep(2)
lcd.clear()
dtime = datetime.datetime.now()

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
lcd.message('Look at the \n camera and wait')

#insert to database
facesql = "INSERT INTO test (userID, userName, timeDate) VALUES (%s, %s, %s)"
faceval = (face_id, face_name, dtime)
mycursor.execute(facesql, faceval)
mydb.commit() 
#insertOrUpdate(face_id, face_name)

#collect 30 face samples
count = 0
while(True):
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the folder
        cv2.imwrite("facedb/" + str(face_name) + '.' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)	

        cv2.imshow('image', frame)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break


# Do a bit of cleanup
lcd.clear()

print("\n [INFO] Exiting Program and cleanup stuff")
lcd.message('Face Registered')

cam.release()
cv2.destroyAllWindows()
