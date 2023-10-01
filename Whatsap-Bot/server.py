import base64
import numpy as np
from flask import Flask, request, jsonify
import face_recognition
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from PIL import Image
import mysql.connector
import cv2
import numpy as np
import face_recognition
from retinaface import RetinaFace


app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app)



def get_face_locations(image_path):
    image = cv2.imread(image_path)
    faces = RetinaFace.detect_faces(image)
    face_locations = []
    for face in faces.values():
       x1, y1, x2, y2 = face['facial_area']
       face_locations.append((y1, x2, y2, x1))  # Convert RetinaFace format to face_recognition format
    return face_locations

def get_face_encodings(image_path, face_locations):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings


def databaseRead(face_encodings_image):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12344321",
        database="TRACKFLIX"
        )

    # Create a cursor object to execute SQL queries
    cursor = db.cursor()
    # Retrieve known face encodings from the database
    cursor.execute(
        "SELECT face_encodes, name,crime, additional_info FROM criminals;")
    rows = cursor.fetchall()
    known_encodings = []
    names = []
    crimes = []
    additionalInfos = []

    for row in rows:
        encoding = np.frombuffer(row[0], dtype=np.float64)
        NAME = row[1]
        CRIME = row[2]
        ADITIONAL_INFO = row[3]
        # Add the face encoding and timestamp to the lists
        known_encodings.append(encoding)
        names.append(NAME)
        crimes.append(CRIME)
        additionalInfos.append(ADITIONAL_INFO)
    # Compare the input face with known faces
    for input_face_encoding in face_encodings_image:
        # Compare the input face encoding with all known face encodings
        
        matches = face_recognition.compare_faces(known_encodings, input_face_encoding,tolerance=0.5)
        # Find the indexes of matching faces
        matching_indexes = [i for i, match in enumerate(matches) if match]

        for matching_index in matching_indexes:
            # Retrieve the name and detail for the matching face
            matching_name = names[matching_index]
            matching_crime = crimes[matching_index]
            matchingaditional_infos = additionalInfos[matching_index]
            return {"name": matching_name, "crime": matching_crime, "additionalInfo": matchingaditional_infos}
        return 'Writting in the database...'
    
        
def dbwrite(Y, Z, a, b):
    # connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12344321",
        database="TRACKFLIX"
    )
    mycursor = mydb.cursor()
    query = "INSERT INTO criminals (face_encodes, name,crime, additional_info) VALUES ( %s, %s, %s, %s)"
    values = (Y, Z, a, b)
    mycursor.execute(query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()


def process_image(file_path):
        # Find faces in the image
    face_locations = get_face_locations(file_path)

    if len(face_locations) > 0:
        
            # Encode the first face found
        face_encodingsa = get_face_encodings(file_path,face_locations)
            # Perform actions with the face encoding
        return databaseRead(face_encodingsa)
    else:
        return 'No face found in the image!'


@app.route('/dbwrite', methods=['POST'])
def process_image_route():
    global file_path_image
    fileName = request.form['fileName']
    file_path_image = os.path.abspath(fileName)

    # Check if the file exists and wait until it is fully saved
    while not os.path.exists(file_path_image):
        pass
    
    result = process_image(file_path_image)
    return result

@app.route('/store', methods=['POST'])
def store():
    
    # Create a cursor object to execute SQL queries
    file_path = request.form['fileName']
    name = request.form['name']
    crime = request.form['crime']
    additionalInfo = request.form['additionalInfo']
    if os.path.isfile(file_path):
        # Open the image and convert it to RGB
        # Find faces in the image
        face_locations = get_face_locations(file_path)
        if len(face_locations) > 0:
            # Encode the first face found
            face_encodings = get_face_encodings(file_path, face_locations)[0]
            dbwrite(face_encodings.tobytes(), name, crime, additionalInfo)
            return "Succesfully Stored"
    return "Failed!"


@app.route('/dbsearch', methods=['POST'])
def dbsearch():
    # connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12344321",
        database="TRACKFLIX"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select face_encodes, name, crime, additional_info from criminals")
    rows = mycursor.fetchall()

    # Load the image into face_recognition librarys
    fileName = request.form['fileName']

    # # Find faces in the image
    face_locations = get_face_locations(fileName)
    face_encodings = get_face_encodings(fileName,face_locations)
    known_encodings = []
    names = []
    crimes = []
    additionalInfos = []
    
    for row in rows:
        # Compare the input face encoding with all known face encodings
        face_encoding = np.frombuffer(row[0], dtype=np.float64)
        
        NAME = row[1]
        CRIME = row[2]
        ADITIONAL_INFO = row[3]
        #Add the face encoding and timestamp to the lists
        known_encodings.append(face_encoding)
        names.append(NAME)
        crimes.append(CRIME)
        additionalInfos.append(ADITIONAL_INFO)

    for input_face_encoding in face_encodings:
        # Compare the input face encoding with all known face encodings
        matches = face_recognition.compare_faces(known_encodings, input_face_encoding,tolerance=0.5)

    # Find the indexes of matching faces
        matching_indexes = [i for i, match in enumerate(matches) if match]

        for matching_index in matching_indexes:
            matching_name = names[matching_index]
            matching_crime = crimes[matching_index]
            matchingaditional_infos = additionalInfos[matching_index]
            return {"name": matching_name, "crime": matching_crime, "additionalInfo": matchingaditional_infos}
    mydb.commit()
    mycursor.close()
    mydb.close()

    if len(face_locations) ==0:
        return "no face in the image"
    
    return "Face not found in the database!"


if __name__ == '__main__':
    app.run()
