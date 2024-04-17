# Face-Attendance-System-python project
## Project overview
### Description
The Face Attendance System is an automated solution for tracking and managing attendance using facial recognition technology. Instead of traditional methods like manual attendance registers or ID cards, this system offers a more convenient and efficient way to record attendance.

### Key Features
1. Facial Recognition: Utilizes face recognition algorithms to identify individuals.
2. Real-time Attendance: Captures attendance in real-time as individuals enter the designated area.
3. Database Integration: Integrates with databases to store and manage information about students or employees.
4. Automatic Recording: Automatically records attendance when recognized faces are detected.
5. Reporting: Generates CSV file for datewise attendance record & keep track of total attendance of each student in realtime database.

### Technologies Used
1. Python: Programming language used for development. 
2. OpenCV: Library for computer vision tasks, including face detection and recognition.
3. Face Recognition Library: Provides pre-trained models and algorithms for face recognition.
4. Firebase: Database and storage solution for storing user information and attendance data.
5. Pandas: Library for data manipulation and analysis.
6. CVZone: Library for computer vision utilities and enhancements.

### Usage
#### Installation and Setup
Install the required dependencies:
   ##### pip install -r requirements.txt  
   
   ##### OR use conda environment commands
   1. conda install cmake
   2. conda install -c conda-forge dlib
   3. pip install face_recognition
   
#### Database
1. Connect the Database
2. Populate Student Information into database using databse.py file
   #####  database.py
3. Upload images of users to the database. These images will be used as reference points for facial recognition during attendance tracking.
   #####  UploadImagetoDb.py
   
#### Image data prepration
Loading Image,Id from the image_details.csv file , image_details.csv file basically mapping image name and Id of the student.

#### Generate Encodings
This step involves extracting facial encodings from a set of images containing faces of individuals whose attendance needs to be tracked. These encodings are numerical representations of facial features and are used for matching faces during attendance tracking. After extracting the encodings EncodeFile.p file is used to store all those encodings.
   ##### encoding.py
   ##### EncodeFile.p (keep encodings)

#### Main Application
Launch the main application script responsible for real-time face detection, recognition, and attendance tracking. This is the core component of the Face Attendance System that users interact with during operation.It also create datewise csv file of student attendance marked present or not with time.
   ##### main.py



