# Import necessary libraries
import socket
from urllib import request

from flask import Flask, render_template, Response, request
import cv2

# Initialize the Flask app
app = Flask(__name__)
#camera = cv2.VideoCapture(2)

camera = cv2.VideoCapture(2, cv2.CAP_GSTREAMER)

out_send = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency,width=640,height=480 bitrate=500 '
                           'speed-preset=superfast ! rtph264pay ! udpsink drop=1 host=127.0.0.1 port=5000',
                           cv2.CAP_GSTREAMER,0, 20, (640,480), True)

def socket_receive():

    while True:
        HOST = "192.168.178.124"  # The server's hostname or IP address
        PORT = 65432  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")
            cords = s.recv(1024)

            return cords


def gen_frames():
    while True:

#        cords = socket_receive()
        success, frame = camera.read()  # read the camera frame
#        print(frame)
#        frame = cv2.rectangle(frame, (5, 5), (120, 120), (255, 0, 0), 2)
#        frame = cv2.rectangle(frame, (cords[4], cords[5]), (cords[6], cords[7]), (255, 0, 0), 2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            out_send.write(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('start_stop') == 'ST_ST':
            pass
        elif request.form.get('action2') == 'Start/Stop':
            pass
        else:
            pass
    elif request.method == 'GET':

        return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
