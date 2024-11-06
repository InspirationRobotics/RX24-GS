import time
import requests
from ground_core import GroundStation, FlaskApp

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
    msg = (msg.split("*")[0])[-3]

    data = {
        'colors': msg,
    }

    # Send the POST request with the new colors
    response = requests.post(flask_url, json=data)

def startFlask():
    flaskApp = FlaskApp()
    flaskApp.run()

if __name__ == "__main__":
    flask_url = 'http://127.0.0.1:5000/update_colors'
    startFlask()
    time.sleep(2)
    STC_msg_callback("RXCOD,051124,213447,INSP,RBG*15")

# if __name__ == "__main__":

#     flaskApp = None
#     flask_url = 'http://127.0.0.1:5000/update_colors'

#     gs = GroundStation("192.168.3.100", 5000, debug=True)
#     gs.add_callback("RXHRB", system_msg_callback)
#     gs.add_callback("RXCOD", STC_msg_callback)

#     while True:
#         time.sleep(1)
#         pass