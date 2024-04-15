import cv2
import os
import pickle
import cvzone
import numpy as np
import face_recognition
from datetime import datetime 


import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

data=pd.read_csv('images_details.csv')

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{"databaseURL" : "https://faceattendancesystem-c7d5a-default-rtdb.firebaseio.com/",
 "storageBucket" : "faceattendancesystem-c7d5a.appspot.com"
}
)

modeType=0
counter=0
imgStudent=[]

cap = cv2.VideoCapture(0)  # Use 0 or -1 for default camera

cap.set(3, 640)
cap.set(4, 480)

file=open("EncodeFile.p","rb")
encode_list_known_with_ids=pickle.load(file)
file.close()
encodings,ids=encode_list_known_with_ids


folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))


while True:
    success, image = cap.read()
    image=cv2.resize(image,(0,0),None,1,1)
    # Convert the resized image to RGB (face_recognition uses RGB images)
      
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faceCurrFrame=face_recognition.face_locations(image)
    encodeCurrFrame=face_recognition.face_encodings(image,faceCurrFrame)
    #cv2.imshow("Webcam", image)
    imgBackground = cv2.imread('background.png')
    
    image_new=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    imgBackground[162:162+480, 55:55+640] = image_new
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    if not success:
        print("Error: Failed to read frame from camera.")
        break

   

    for encodeFace,faceLoc in zip(encodeCurrFrame,faceCurrFrame):
        matches=face_recognition.compare_faces(encodings,encodeFace)
        faceDist=face_recognition.face_distance(encodings,encodeFace)
        print("matches",matches)
        print("dist",faceDist)

        matchIndex=np.argmin(faceDist)
        if matches[matchIndex] and faceDist[matchIndex] < 0.40:


            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 , x2 , y2 , x1
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            # print("roll_no",ids[matchIndex])
            
            if counter==0:
                id=ids[matchIndex]
                counter=1
                modeType=1  
    
    if counter!=0:
        
        if counter==1:
            # data
            studentInfo= db.reference(f"Students/{id}").get()
            print(studentInfo)

            # image
            
            image_value = data.loc[data['id'] == id, 'image'].values[0]
            bucket=storage.bucket()
            blob = bucket.get_blob(f'images/{image_value}')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
            imgStudent=cv2.resize(imgStudent,(216,216))

            # update attendance
            ref=db.reference(f"Students/{id}")
            # studentInfo['total_attendance']+=1
            # ref.child('total_attendance').set(studentInfo['total_attendance'])
            datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            print(secondsElapsed)
            if secondsElapsed > 20:
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType = 3
                counter = 0
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if modeType!=3:     
               
        
            if 5 < counter <10 :
                modeType=2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    
                
            if counter<=5:
                cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
    
                cv2.putText(imgBackground,str(studentInfo['course']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    
                cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    
                cv2.putText(imgBackground,str(studentInfo['enrolled_year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
    
                #cv2.putText(imgBackground,str(studentInfo['enrolled_year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                imgBackground[175:175 + 216, 909:909 + 216] = imgStudent 

        

            counter =counter+ 1
    
            if counter > 10:
                counter=0
                modeType=0
                studentInfo=[]
                imgStudent=[]
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


   
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

