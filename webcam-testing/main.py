import cv2
import zmq
from time import sleep

port = 5556
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect(f"tcp://127.0.0.1:{port}")
def send_data(port, data):
    socket.recv()
    print(f"Sending data: {data}")
    socket.send(data.encode())

def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

cameras = returnCameraIndexes()
print(cameras)
assert len(cameras) > 0, "no cameras detected"

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

video_capture = cv2.VideoCapture(cameras[0])

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    print(frame.shape)
    print(ret)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE 
    )

    # Draw a rectangle around the faces
    if len(faces) == 0:
        # message = socket.recv()
        i=-1
        pos_out = f"FACE{i}:{-1};"

        send_data(port=5556, data=pos_out)

    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #  Send reply back to client
        # message = socket.recv()
        pos_out = f"FACE{i}:{x};"
        send_data(port=5556, data=pos_out)

        # socket.send(pos_out)
    
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()