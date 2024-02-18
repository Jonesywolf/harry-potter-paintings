from flask import Flask, request
import serial

app = Flask(__name__)

# Door states: open, close
DOOR_OPEN = "DOOR_OPEN"
DOOR_CLOSED = "DOOR_CLOSED"
# Light states: on, off
LIGHT_ON = "LIGHT_ON"
LIGHT_OFF = "LIGHT_OFF"

# State of the light and door
state = {
    'light': LIGHT_OFF,
    'door': DOOR_CLOSED
}

def send_arduino_command(command):
    # Add a newline character to the command
    command = command + '\n'
    # Encode the command to bytes and send it over the serial connection
    global arduino_serial
    arduino_serial.write(command.encode())

import serial.tools.list_ports

def find_serial_device():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        try:
            ser = serial.Serial(p.device, 9600)  # Adjust the baud rate as needed
            print(f"Successfully connected to {p.device}")
            return ser
        except:
            print(f"Failed to connect to {p.device}")
    return None

arduino_serial = find_serial_device()
if arduino_serial is None:
    print("No available serial devices")
    exit(1)
send_arduino_command(state['light'])

@app.route('/control/light', methods=['POST'])
def control_light():
    try:
        requested_state = request.json.get('state')
        if requested_state not in [LIGHT_ON, LIGHT_OFF]:
            return 'Invalid light state', 400
        state['light'] = requested_state
    except Exception as e:
        return str(e), 400
    send_arduino_command(state['light'])
    return f'Light turned {state["light"]}'

@app.route('/control/door', methods=['POST'])
def control_door():
    try:
        requested_state = request.json.get('state')
        if requested_state not in [DOOR_OPEN, DOOR_CLOSED]:
            return 'Invalid door state', 400
        state['door'] = requested_state
    except Exception as e:
        return str(e), 400
    send_arduino_command(state['door'])    
    return f'Door {state["door"]}'

if __name__ == '__main__':
    app.run(port=5000, debug=True)