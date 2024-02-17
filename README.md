# Harry Potter Paintings Brought To Life
Harry Potter Paintings brought to life, the perfect addition to your smart home.

## Project Planning
We can do multiple face detection using OpenCV, then we can use those bounding boxes to capture an image of a person's face. We then attempt to perform facial recognition.
If we don't get a match, we generate a new ID for them.

Using the images of the person's face that we captured, we can store a unique identifier for them and store their face locally and then upload it to the server.

### The central server
The server maintains a repository of faces so that all devices can access a common database of faces for recognition.
Each person is assigned a character in the painting. They spawn in with the same x (at least relatively, the camera width and screen width might be a different number of pixels) position on the screen as the detected person in the camera (might have to mirror this).

The server also has to be initialized with client IDs for each painting 

The server could live on one of our laptops or its own Pi, we'll see.

### Game engine
Unity is really powerful, especially for lighting but the Raspberry Pis are annoying to deploy to (across our laptops and the Pi, that's 3 OSes so 3 different builds). Plus, my laptop has integrated graphics so using the Unity Editor at all would be tough. So instead, we'll use Pygame which will make it easy to do everything in one script (communicate with the Arduinos/control the GPIO, run facial recognition/detection, communicate with the servers, and obviously, control the characters). Also, Unity might be too processor-intensive for the Pis.

### Add Arduinos to laptops?
The Raspberry Pis could control LEDs (meant to represent the lights of your house) directly, and we could add Arduinos so the laptops can do the same thing. Perhaps we can come up with more exciting physical interactions but that's all I've got for now.

### Fun additions
If the characters could randomly 

## To Do
### Camera Stuff
[ ] Facial Detection with webcam
[ ] Facial Recognition with webcam
[ ] Combine the above
[ ] Run it on a Raspberry Pi
### Raspberry Pi Setup
[ ] Use a camera on Raspberry Pis
[ ] Get touchscreens working on Raspberry Pis
[ ] Get Pis connected to Wifi
### Server stuff
[ ] Test local connections using an Ethernet Switch
[ ] Investigate how to send images, do we need a database?
[ ] See if you can run it on a Raspberry Pi 



