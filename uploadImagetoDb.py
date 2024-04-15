import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{"databaseURL" : "https://faceattendancesystem-c7d5a-default-rtdb.firebaseio.com/",
 "storageBucket" : "faceattendancesystem-c7d5a.appspot.com"
}
)


data= pd.read_csv("images_details.csv")
for i in range(len(data)):
    imgPath=f"images/{data['image'][i]}"
    bucket=storage.bucket()
    blob=bucket.blob(imgPath)
    blob.upload_from_filename(imgPath)
