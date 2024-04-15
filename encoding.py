import pandas as pd 
import numpy as np 
import cv2
import face_recognition 
import pickle
from train_data import imageData

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import storage

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred,
# {"databaseURL" : "https://faceattendancesystem-c7d5a-default-rtdb.firebaseio.com/",
#  "storageBucket" : "faceattendancesystem-c7d5a.appspot.com"
# }
# )

# Initialize imageData object
image_data = imageData()

# Iterate through each image to extract face encodings and IDs
def find_encodings():
    length = image_data.length()
    known_face_encodings = []
    known_face_ids = []
    for i in range(length):
        # Get the image and its corresponding ID
        image, id = image_data.get_image(i)
        
        # Encode the face in the image
        face_encodings = face_recognition.face_encodings(image)
        
        # Check if any face was detected
        if len(face_encodings) > 0:
            # Append the first face encoding and its corresponding ID to the lists
            known_face_encodings.append(face_encodings[0])
            known_face_ids.append(id)
        else:
            print(f"No face detected in image {i + 1}. Skipping.")

    return known_face_encodings, known_face_ids    

print("Encoding start")
encoding_list_known, student_ids = find_encodings()
print("Encoding complete")

encode_list_known_with_ids = [encoding_list_known, student_ids]

file = open("EncodeFile.p", "wb")
pickle.dump(encode_list_known_with_ids, file)
file.close()
print("File saved")
