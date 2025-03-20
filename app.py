from flask import Flask, render_template, Response
import cv2
import numpy as np
from deepface import DeepFace

app = Flask(__name__)

# Initialize camera
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Vital Sign and Emotion Detection Logic
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Emotion Analysis
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)[0]
                emotion = result['dominant_emotion']
                cv2.putText(frame, f'Emotion: {emotion}', (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            except:
                cv2.putText(frame, 'Emotion: N/A', (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Display the frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera.html')
def camera_feed():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
