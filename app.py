# Import necessary libraries
import socket
from urllib import request
import pickle
import time
from flask import Flask, render_template, Response, request
import cv2

IM_WIDTH = 640
IM_HEIGHT = 480
fps = 30

# Initialize the Flask app
app = Flask(__name__)
# camera = cv2.VideoCapture(2)

camera = cv2.VideoCapture(2, cv2.CAP_GSTREAMER)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, IM_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IM_HEIGHT)
camera.set(cv2.CAP_PROP_FPS, fps)
camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
camera.set(28, 15)


out_send = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency,width=640,height=480 bitrate=500 '
                           'speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=4200',
                           cv2.CAP_GSTREAMER,2, 20, (640,480), True)


@app.route('/socket', methods=['POST'])
def socket_receive():

    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 9090  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        pick = s.recv(1024)
        msg = pickle.loads(pick)
        sample_output = msg

        return sample_output


def gen_frames():
    difficulty = 'normal'
    while True:
        success, frame = camera.read()  # read the camera frame
        out_send.write(frame)
#        time.sleep(5)
#        cords = socket_receive()
#        print(cords)
#        if difficulty == 'normal':
#            time.sleep(2)
#
#        elif difficulty == 'hard':
#            time.sleep(1)

#        elif difficulty == 'easy':
#            time.sleep(4)
#        frame = cv2.rectangle(frame, (cords[0], cords[1]), (cords[2], cords[3]), (255, 0, 0), 2)
#        frame = cv2.rectangle(frame, (cords[4], cords[5]), (cords[6], cords[7]), (255, 0, 0), 2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'Start':
            pass
        elif request.form.get('action2') == 'VALUE2':
            pass  # do something else
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


@app.route("/test", methods=['GET', 'POST'])
def test():
    select = str(request.form.get('Schwierigkeitsgrad'))
    return str(select)  # just to see what select is


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
