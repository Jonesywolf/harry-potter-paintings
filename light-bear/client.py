import requests
import time

# Specify the local server url
url = "http://localhost:5000"

# Door states: open, close
DOOR_OPEN = "DOOR_OPEN"
DOOR_CLOSED = "DOOR_CLOSED"
# Light states: on, off
LIGHT_ON = "LIGHT_ON"
LIGHT_OFF = "LIGHT_OFF"


def control_light(state):
    if state not in [LIGHT_ON, LIGHT_OFF]:
        raise ValueError("Invalid light state")
    data = {'state': state}
    response = requests.post(url + "/control/light", json=data)
    print(response.text)

def control_door(state):
    if state not in [DOOR_OPEN, DOOR_CLOSED]:
        raise ValueError("Invalid door state")
    data = {'state': state}
    response = requests.post(url + "/control/door", json=data)
    print(response.text)

if __name__ == "__main__":
    while True:
        control_light(LIGHT_ON)
        time.sleep(1)
        control_light(LIGHT_OFF)
        time.sleep(1)