import cv2
import os
import os.path
import mysql.connector

mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing" 
    )

mycursor = mydb.cursor()
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n Enter User ID: <return> ==>  ')
face_name = input('\n Enter Name:')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
folder = ("Dataset/" + str(face_name))
os.mkdir(folder)
os.chdir(folder)

facesql = "INSERT INTO facelog (ID, Name, ImagePath) VALUES (%s, %s, %s)"
faceval = (face_id, face_name, folder)
mycursor.execute(facesql, faceval)
mydb.commit() #execute the sql query
count = 0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the folder
       
        cv2.imwrite(str(face_name)+ '.' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 20: # Take 20 face sample and stop video
         break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()