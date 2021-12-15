import os
face_id = input('\n Enter User ID: <return> ==>  ')
face_name = input('\n Enter Name:')
folder = ("Dataset/" + str(face_name))
os.mkdir(folder)