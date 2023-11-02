from flask import Flask, render_template
import cv2
import os

app = Flask(__name__)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/runcaptureimage')
def run_captureimage():
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        ret, frame = cap.read()
        print(ret)
        print(frame)
    else:
        ret = False

    img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    directory = os.getcwd()
    os.chdir(directory)
    print(os.listdir(directory)) 
    filename = 'Intruder.jpg'
    cv2.imwrite(os.path.join(directory, filename), img1) 

    cap.release()
    return "Capture image executed successfully!"

if __name__ == '__main__':
    app.run()
