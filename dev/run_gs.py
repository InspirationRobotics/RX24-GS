import time
import requests
from ground_core import GroundStation, FlaskApp
from threading import Thread
import random

def system_msg_callback(msg):
    '''
    This is an example of how a callback would work. 
    This function is called whenever a system message is received (denoted by the message id RXPTH)
    Note that this is a blocking function so nothing with loops or sleeps should be done here.
    '''
    print("System message received: ", msg)
    pass

def STC_msg_callback(msg : str):
    """
    This callback will be triggered for the ScanTheCode mission
    """
    # msg format = $RXCOD,051124,213447,INSP,RBG*15
    msg = (msg.split("*")[0])[-3:]
    data = {
        'colors': msg,
    }

    # Send the POST request with the new colors
    response = requests.post(flask_url, json=data)

def startFlask():
    flaskApp = FlaskApp()
    flaskApp.run()

# def dummy_send():
#     while True:
#         time.sleep(2)
#         characters = ['R', 'B', 'G']
#         random.shuffle(characters)
#         color_string = ''.join(characters)
#         STC_msg_callback(f"RXCOD,051124,213447,INSP,{color_string}*15")

# if __name__ == "__main__":
#     flask_url = 'http://127.0.0.1:5001/update_colors'
#     flaskThread = Thread(target=dummy_send)
#     flaskThread.start()
#     startFlask()

if __name__ == "__main__":

    flask_url = 'http://127.0.0.1:5001/update_colors'

    gs = GroundStation("robot.server", 12345, dummy=True)
    gs.add_callback("RXHRB", system_msg_callback)
    gs.add_callback("RXCOD", STC_msg_callback)

    startFlask()