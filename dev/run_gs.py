from ground_core import GroundStation
from ground_core.light_status import FlaskApp
import requests
flaskApp = None
flask_url = 'http://127.0.0.1:5000/update_colors'

def system_msg_callback(msg):
    '''
    This is an example of how a callback would work. 
    This function is called whenever a system message is received (denoted by the message id RXPTH)
    Note that this is a blocking function so nothing with loops or sleeps should be done here.
    '''
    print("System message received: ", msg)
    
    
    
def lightTower_heartbeat_callback(self, msg):
    """
    This callback will be triggered for the ScanTheCode mission

    """
    
    data = {
        'colors': msg,
    }
    
    # Send the POST request with the new colors
    response = requests.post(flask_url, json=data)
    
def startFlask(self):
    self.flaskApp = FlaskApp()
    self.flaskApp.run()
    
    
    


if __name__ == "__main__":
    gs = GroundStation()
    gs.add_callback("RXPTH", system_msg_callback)
    gs.add_callback("RXCOD", lightTower_heartbeat_callback)