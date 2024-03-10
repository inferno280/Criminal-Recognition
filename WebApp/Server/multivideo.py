import cv2
import numpy as np
import time
import face_recognition

def realtimedown():

    # Load the input image
    input_image = face_recognition.load_image_file("/media/rajasgh18/4e01c188-d741-41d8-979d-d7ba57008d94/Personel/Raja.jpg")

    # Encode the input image
    input_encoding = face_recognition.face_encodings(input_image)[0]

    # Define IP addresses and ports of the webcams
    sources = [
        0,
        0,
        "http://192.168.31.2:8080/video",  # Replace with actual IP addresses
        "http://192.168.31.2:8080/video",  # Replace with actual IP addresses
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

realtimedown()
