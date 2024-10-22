from ground_core import GroundStation

def system_msg_callback(msg):
    '''
    This is an example of how a callback would work. 
    This function is called whenever a system message is received (denoted by the message id RXPTH)
    Note that this is a blocking function so nothing with loops or sleeps should be done here.
    '''
    print("System message received: ", msg)


if __name__ == "__main__":
    gs = GroundStation()
    gs.add_callback("RXPTH", system_msg_callback)