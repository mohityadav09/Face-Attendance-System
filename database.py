import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{"databaseURL" : "https://faceattendancesystem-c7d5a-default-rtdb.firebaseio.com/"}
)

ref=db.reference("Students")

data={
    "220150008":{
        "name":"Mohit Yadav",
        "enrolled_year":2022,
        "course":"Python",
        "last_attendance_time":"2024-04-15 00:55:25",
        "total_attendance":5
    },
    "220150006":{
        "name":"Ravi Teja",
        "enrolled_year":2022,
        "course":"Python",
        "last_attendance_time":"2024-04-15 00:55:25",
        "total_attendance":3
    },
    "220150025":{
        "name":"Nagendra",
        "enrolled_year":2022,
        "course":"Python",
        "last_attendance_time":"2024-04-15 00:55:25",
        "total_attendance":7
    },
    "220150012":{
        "name":"Prince Tholia",
        "enrolled_year":2022,
        "course":"Python",
        "last_attendance_time":"2024-04-15 00:55:25",
        "total_attendance":2
    },
    "220150021":{
        "name":"Onkar",
        "enrolled_year":2022,
        "course":"Python",
        "last_attendance_time":"2024-04-15 00:55:25",
        "total_attendance":6
    },
    "220150036":{
        "name":"Rahul jat",
        "enrolled_year":2022,
        "course":"Python",
        "last_attendance_time":"2024-04-15 00:55:25",
        "total_attendance":3
    }
}

for key,value in data.items():
    ref.child(key).set(value)
