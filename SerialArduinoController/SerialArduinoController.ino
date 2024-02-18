#define LED_PIN LED_BUILTIN
#define LIGHT_ON "LIGHT_ON"
#define LIGHT_OFF "LIGHT_OFF"
#define DOOR_OPEN "DOOR_OPEN"
#define DOOR_CLOSED "DOOR_CLOSED"

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  // Initialize the built-in LED pin as an output
  pinMode(LED_PIN, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
  // Start the serial connection
  Serial.begin(9600);
}
void loop() {
  // Check if data is available to read
  if (Serial.available()) {
    // Read the incoming command
    String command = Serial.readStringUntil('\n');

    // Remove any trailing whitespace
    command.trim();

    // Check the command and update the LED state
    if (command == LIGHT_ON) {
      digitalWrite(LED_PIN, HIGH);
    } else if (command == LIGHT_OFF) {
      digitalWrite(LED_PIN, LOW);
    } else if (command == DOOR_OPEN) {
        myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
        myservo.write(90);
        delay(2000);
        myservo.detach();
    } else if (command == DOOR_CLOSED) {
        myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
        myservo.write(0);
        delay(2000);
        myservo.detach();
    }
  }
}
