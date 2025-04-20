# app.py
from flask import Flask, Response
import cv2

# Initialize Flask app
app = Flask(__name__)

# Open the external camera (use the appropriate camera index)
camera = cv2.VideoCapture(1)  # Usually, '0' is for the default camera, '1' for external camera.

# Check if the camera opened correctly
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

# Function to generate frames for video streaming
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to serve the video stream
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
