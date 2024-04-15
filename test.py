from flask import Flask, render_template, Response
import cv2
import pickle
import face_recognition
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)
file = open("EncodeFile.p", "rb")
encode_list_known_with_ids = pickle.load(file)
file.close()
encodings, ids = encode_list_known_with_ids


def gen_frames():
    resize_factor = 0.25
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break

        # Resize the frame
        resized_frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

        # Convert the resized image to RGB (face_recognition uses RGB images)
        image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        faceCurrFrame = face_recognition.face_locations(image)
        encodeCurrFrame = face_recognition.face_encodings(image, faceCurrFrame)

        face_id = []
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodings, encodeFace)
            faceDist = face_recognition.face_distance(encodings, encodeFace)
            id = 0
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                id = ids[matchIndex]
            face_id.append(id)

        # Display the results
        for (top, right, bottom, left), name in zip(faceCurrFrame, face_id):
            # Scale back up face locations
            top *= int(1 / resize_factor)
            right *= int(1 / resize_factor)
            bottom *= int(1 / resize_factor)
            left *= int(1 / resize_factor)

            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(
                image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                image, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )

        # Convert frame to JPEG format
        ret, buffer = cv2.imencode(".jpg", image)
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + image + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
