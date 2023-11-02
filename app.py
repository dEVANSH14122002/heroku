from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)

# Set up a directory to store captured images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to capture and save image
def capture_image():
    try:
        # Check if camera is available
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Could not access the camera")

        # Capture image
        ret, frame = cap.read()
        cap.release()

        if ret:
            # Save image
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.jpg')
            cv2.imwrite(img_path, frame)
            return img_path
        else:
            raise Exception("Failed to capture image")
    except Exception as e:
        return str(e)

# Route to render the login page
@app.route('/')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
