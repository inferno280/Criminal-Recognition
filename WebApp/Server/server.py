import os
from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
from PIL import Image
from io import StringIO
import cv2
import numpy as np
import face_recognition
import mysql.connector
import os
from datetime import datetime
import time
from flask_socketio import SocketIO, emit
import keyboard
import object_detection.object_detector_live_stream.detect as ai
from sms import message
# from pynput import keyboard

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

app.debug = True


def mysql_connector(db):
    # connect to database
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12344321",
        database=db
    )


@app.route('/process_video', methods=['POST'])
def process_video():
    # connect to database
    mydb = mysql_connector("trackflix")
    mycursor = mydb.cursor()

    # create table to store face encodings and timestamps
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS faces (id INT AUTO_INCREMENT PRIMARY KEY, encoding TEXT, timestamps TEXT)")

    # read video file from request
    video_file = request.files['videoFile']
    video_path = os.path.join(
        "../Client/public/assets/videos", video_file.filename)
    video_file.save(video_path)

    cap = cv2.VideoCapture(video_path)

    # set parameters
    frame_count = 0
    skip_frames = 10
    resize_factor = 0.25

    # loop through frames
    while cap.isOpened():
        # read frame
        ret, frame = cap.read()

        # check if end of video
        if not ret:
            break

        # skip frames
        if frame_count % skip_frames != 0:
            frame_count += 1
            continue

        # resize frame
        resized_frame = cv2.resize(
            frame, None, fx=resize_factor, fy=resize_factor)

        # detect faces
        face_locations = face_recognition.face_locations(
            resized_frame, model='hog')

        # encode faces
        face_encodings = face_recognition.face_encodings(
            resized_frame, face_locations)

        # write face encodings and timestamps to database
        if len(face_encodings) > 0:
            timestamps = str(int(cap.get(cv2.CAP_PROP_POS_MSEC) // 1000))
            for face_encoding in face_encodings:
                encoding_str = ','.join([str(val) for val in face_encoding])
                sql = "INSERT INTO faces (encoding, timestamps) VALUES (%s, %s)"
                val = (encoding_str, ''.join(timestamps))
                mycursor.execute(sql, val)

        # increment frame count
        frame_count += 1

        # speed up video playback
        cv2.waitKey(1)

    # release video capture and close database connection
    cap.release()
    mydb.commit()
    mycursor.close()
    mydb.close()

    # delete video file from disk
    # os.remove(video_path)

    return 'success'


@app.route('/detect', methods=['POST'])
@cross_origin()
def detect_face():
    # connect to database
    mydb = mysql_connector("trackflix")
    mycursor = mydb.cursor()

    # get image file from request
    image_file = request.files['image']

    # load known face
    known_image = face_recognition.load_image_file(image_file)
    known_encoding = face_recognition.face_encodings(known_image)[0]

    # search for known face in database
    mycursor.execute("SELECT * FROM faces")
    results = mycursor.fetchall()
    timestamps = []
    for result in results:
        encoding = result[1].split(',')
        encoding = [float(val) for val in encoding]
        face_encoding = [encoding[i:i+128]
                         for i in range(0, len(encoding), 128)][0]
        distance = face_recognition.face_distance(
            [face_encoding], known_encoding)[0]
        if distance < 0.6:
            timestamps += [int(timestamp)
                           for timestamp in result[2].split(',')]

    # close database connection
    mycursor.close()
    mydb.close()

    # return timestamps in JSON format
    if timestamps:
        response = {
            'message': "success",
            'timestamps': timestamps
        }
    else:
        response = {'message': "failed"}
    return jsonify(response)


@app.route('/realtime', methods=["POST"])
def realtime():
    # Load the input image
    input_image = face_recognition.load_image_file(request.files['image'])

    # Encode the input image
    input_encoding = face_recognition.face_encodings(input_image)[0]

    # Initialize the video capture
    video_capture = cv2.VideoCapture(0)

    # Initialize the variables for tracking face entry and exit time
    face_enter_time = None
    face_exit_time = None

    resultList = []

    # Iterate over frames from the video stream
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Convert the frame from BGR color (OpenCV default) to RGB color
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations)

        # Iterate over the detected faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the face encoding with the input image encoding
            matches = face_recognition.compare_faces(
                [input_encoding], face_encoding)
            name = "Unknown"

            if matches[0]:
                if name == "Unknown":

                    start_time_found = time.time()

                name = "User"
                # Print entry time if the user is found
                if face_enter_time is None:
                    face_enter_time = time.ctime()
                    resultList.append("Face entered at:" + face_enter_time)

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Write the name of the user or "Unknown" on the frame
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Print exit time if the face is no longer detected
        if face_enter_time is not None and len(face_locations) == 0:
            if face_exit_time is None:
                face_exit_time = time.ctime()
                resultList.append("Face exited at:" + face_exit_time)
                face_enter_time = None
                face_exit_time = None

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the video capture and close all windows
    video_capture.release()
    cv2.destroyAllWindows()
    if len(resultList) != 0:
        response = {
            'message': "success",
            'timestamps': resultList
        }
    else:
        response = {'message': "failed"}
    return jsonify(response)


@app.route('/realtime-download', methods=["POST"])
def realtimedown():

    # Load the input image
    input_image = face_recognition.load_image_file(request.files['image'])

    # Encode the input image
    input_encoding = face_recognition.face_encodings(input_image)[0]

    # Define IP addresses and ports of the webcams
    sources = [
        0,
        "http://192.168.31.2:8080/video",  # Replace with actual IP addresses
        "http://192.168.31.2:8080/video",  # Replace with actual IP addresses
        "http://192.168.31.228:8080/video",  # Replace with actual IP addresses
        # "192.168.31.2",
        # "192.168.31.2"
        # Add more IP addresses as needed
    ]

    # Create video capture objects for each webcam
    caps = [cv2.VideoCapture(source) for source in sources]

    # Initialize variables for tracking face entry and exit time for each webcam
    face_enter_times = [None] * len(caps)
    face_exit_times = [None] * len(caps)
    frames_lists = [[] for _ in range(len(caps))]
    results_lists = [[] for _ in range(len(caps))]

    while True:
        frames = []

        for i, video_capture in enumerate(caps):
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            # If frame is not available, continue to the next iteration
            if not ret:
                continue

            # Resize frame to a smaller resolution
            frame = cv2.resize(frame, (600, 400))

            # Convert the frame from BGR color (OpenCV default) to RGB color
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find all face locations and encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Iterate over the detected faces
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face encoding with the input image encoding
                matches = face_recognition.compare_faces([input_encoding], face_encoding)
                name = "Unknown"

                if matches[0]:
                    name = "User"
                    if face_enter_times[i] is None:
                        face_enter_times[i] = time.ctime()
                        timestamp = int(time.time())
                        filename = f"photo_{timestamp}.jpg"
                        # Save the frame as an image file
                        cv2.imwrite("../Client/public/assets/realtimeFrames/"+filename, frame)
                        # Add filename to the frames list
                        frames_lists[i].append(filename)

                        # Emit the detected face frame
                        # socketio.emit('face_detected_frame', {'frameName': filename})
                        # message("+919926685773", "Person found!!! Go check on the website for more details.")

                    # Draw a rectangle around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Write the name of the user or "Unknown" on the frame
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Check if face has exited
            if face_enter_times[i] is not None and len(face_locations) == 0:
                if face_exit_times[i] is None:
                    face_exit_times[i] = time.ctime()
                    results_lists[i].append("Face exited at:" + face_exit_times[i])

            frames.append(frame)

        # Determine the number of rows and columns in the grid
        num_rows = int(np.ceil(len(frames) ** 0.5))
        num_cols = int(np.ceil(len(frames) / num_rows))

        # Create a blank canvas to display the grid of webcam feeds
        canvas_height = num_rows * frames[0].shape[0]
        canvas_width = num_cols * frames[0].shape[1]
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

        # Arrange frames in a grid on the canvas
        for i, frame in enumerate(frames):
            row = i // num_cols
            col = i % num_cols
            y_start = row * frames[0].shape[0]
            y_end = (row + 1) * frames[0].shape[0]
            x_start = col * frames[0].shape[1]
            x_end = (col + 1) * frames[0].shape[1]
            canvas[y_start:y_end, x_start:x_end] = frame

        # Display the grid of webcam feeds
        cv2.imshow("Webcam Feeds", canvas)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture objects and close all windows
    for video_capture in caps:
        video_capture.release()
    cv2.destroyAllWindows()

    # Return any collected data
    response = {
        'message': 'success',
        'timestamps': results_lists,
        'frames': frames_lists
    }

    return response


@app.route('/database-encode', methods=['GET'])
def databaseEncode():
    # Connect to the MySQL database
    db = mysql_connector("trackflix")

    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # Create a table to store face encodings and timestamps
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS face_encodings (id INT AUTO_INCREMENT PRIMARY KEY, encoding LONGBLOB, timestamp DATETIME)")

    # Initialize variables
    timestamps = []

    # Load a sample image for face comparison (optional)
    # known_image = face_recognition.load_image_file("known_face.jpg")
    # known_encoding = face_recognition.face_encodings(known_image)[0]

    # Start video capture
    video_capture = cv2.VideoCapture(2)

    # Check if the camera is opened
    if not video_capture.isOpened():
        print("Unable to open camera.")
        exit()

    # Run the loop until a specific key is pressed
    while True:
        # Read each frame of the video
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture frame.")
            break

        # Resize the frame to improve processing speed (optional)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the frame from BGR to RGB
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            # Encode the faces in the frame
            face_encodings = face_recognition.face_encodings(
                rgb_frame, face_locations)

            # Get the current timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for face_encoding in face_encodings:
                # Store the face encoding and timestamp in the database
                sql = "INSERT INTO face_encodings (encoding, timestamp) VALUES (%s, %s)"
                val = (face_encoding.tobytes(), current_time)
                cursor.execute(sql, val)
                db.commit()

                # Add the timestamp to the timestamps array
                timestamps.append(current_time)

        # Display the resulting image with face rectangles
        for (top, right, bottom, left) in face_locations:
            # Scale back the face locations to the original size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display the resulting image
        # cv2.imshow('Video', frame)

        # Check if the specified key is pressed to break the loop
        # pressed = False
        # def onPress(key):
        #     if key == keyboard.Key.esc:
        #         # Stop listener
        #         pressed = True
        #         return
        # with keyboard.Listener(on_press=onPress) as listener:
        #     listener.join()
        if keyboard.is_pressed('esc'):  # Change 'esc' to the desired key
            break

    # Release the video capture and close the windows
    video_capture.release()
    cv2.destroyAllWindows()

    # Close the database connection
    cursor.close()
    db.close()
    return {"message": "closed"}


@app.route('/database-read', methods=['POST'])
def databaseRead():
    # Connect to the MySQL database
    db = mysql_connector("trackflix")

    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # Load the input image
    input_image = face_recognition.load_image_file(request.files['image'])

    # Detect faces in the input image
    input_face_locations = face_recognition.face_locations(input_image)
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations)

    # Retrieve known face encodings from the database
    cursor.execute("SELECT encoding, timestamp FROM face_encodings")
    rows = cursor.fetchall()

    known_encodings = []
    timestamps = []
    matchedTimestamps = []

    for row in rows:
        encoding = np.frombuffer(row[0], dtype=np.float64)
        timestamp = row[1]

        # Add the face encoding and timestamp to the lists
        known_encodings.append(encoding)
        timestamps.append(timestamp)

    # Compare the input face with known faces
    for input_face_encoding in input_face_encodings:
        # Compare the input face encoding with all known face encodings
        matches = face_recognition.compare_faces(
            known_encodings, input_face_encoding)

        # Find the indexes of matching faces
        matching_indexes = [i for i, match in enumerate(matches) if match]

        for matching_index in matching_indexes:
            # Retrieve the timestamp for the matching face
            matching_timestamp = timestamps[matching_index]
            matchedTimestamps.append(
                f"Matching face found at: {matching_timestamp}")

    # Close the database connection
    cursor.close()
    db.close()

    if len(matchedTimestamps) != 0:
        return {
            'message': 'success',
            'timestamps': matchedTimestamps
        }
    else:
        return {'message': 'failed'}


@app.route('/media-pipe', methods=['GET'])
def media_pipe():
    print("test")
    ai.main()
    print("Success")
    return "Success"


@app.route('/', methods=['GET'])
def index():
    return "Welcome to Trackflix API!"


if __name__ == '__main__':
    app.run()
