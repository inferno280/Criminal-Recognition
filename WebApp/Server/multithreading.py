import cv2
import numpy as np
# Define IP addresses and ports of the webcams
ip_addresses = [
    "192.168.31.2",  # Replace with actual IP addresses
    # "192.168.31.2",
    # "192.168.31.2"
    # Add more IP addresses as needed
]
port = 8080  # Port used by IP webcams

# Create video capture objects for each webcam
caps = [cv2.VideoCapture(f"http://{ip}:{port}/video") for ip in ip_addresses]

# Calculate the number of rows and columns for the grid layout
num_webcams = len(caps)
num_cols = int(num_webcams ** 0.5)
num_rows = (num_webcams + num_cols - 1) // num_cols

while True:
    # Read frames from each webcam
    frames = [cap.read()[1] for cap in caps]

    # Resize frames to have the same dimensions
    frames = [cv2.resize(frame, (320, 240)) for frame in frames]

    # Create a blank canvas to display all webcam feeds in a grid layout
    canvas_height = num_rows * 240
    canvas_width = num_cols * 320
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

    # Place frames on the canvas in a grid layout
    for i, frame in enumerate(frames):
        row = i // num_cols
        col = i % num_cols

        # Calculate coordinates for placing the frame in the grid
        x = col * 320
        y = row * 240

        # Place the frame on the canvas
        canvas[y:y+240, x:x+320] = frame

    # Display the canvas with all webcam feeds
    cv2.imshow("Webcam Feeds", canvas)

    # Check for key press every 30 milliseconds
    if cv2.waitKey(30) != -1:
        break

# Release video capture objects and close window
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
