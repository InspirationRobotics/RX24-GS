import time
from ground_core import GroundStation

def system_msg_callback(msg):
    '''
    This is an example of how a callback would work. 
    This function is called whenever a system message is received (denoted by the message id RXPTH)
    Note that this is a blocking function so nothing with loops or sleeps should be done here.
    '''
    print("System message received: ", msg)
    pass


if __name__ == "__main__":
    gs = GroundStation("192.168.3.100", 5000, debug=True)
    gs.add_callback("RXHRB", system_msg_callback)
    while True:
        time.sleep(1)
        pass