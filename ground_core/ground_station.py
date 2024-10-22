import time
from typing import Tuple
from threading import Thread, Lock
from comms_core import Client, Logger, CustomSocketMessage as csm

'''
A pretty simple class that receives a heartbeat from the server, stores it, and then sends it to a 
separate judges server at 1hz. We can add callbacks to run based off the message id.
'''

class GroundStation(Logger):

    def __init__(self, TD_IP, TD_port) -> None:
        super().__init__("GroundStation")
        self.boat_client = Client("192.168.3.2", callback=self._boat_callback)
        self.TD_client = Client(TD_IP, port=TD_port)

        self.mission_heartbeat = None
        self.system_heartbeat = None
        self.callback_list = {}

        self.active = True
        self.send_thread = Thread(target=self._send_heartbeat)
        self.send_lock = Lock()
        self.send_thread.start()

    def add_callback(self, msg_id, callback):
        self.callback_list[msg_id] = callback

    @staticmethod
    def _get_msg_id(msg : str) -> str:
        return msg.split(",")[0][1:]
    
    def _send_heartbeat(self):
        while self.active:
            with self.send_lock:
                self.TD_client.send(self.mission_heartbeat)
                self.TD_client.send(self.system_heartbeat)
                self.mission_heartbeat = None
                self.system_heartbeat = None
            time.sleep(1)

    def _boat_callback(self, msg : str, address : Tuple[str, int]):
        data = csm.decode(msg)
        if data is None:
            return
        mission_heartbeat = data["mission"]
        system_heartbeat = data["system"]
        if mission_heartbeat is not None:
            if GroundStation._validate_checksum(mission_heartbeat):
                with self.send_lock:
                    self.mission_heartbeat = mission_heartbeat
                id = GroundStation._get_msg_id(mission_heartbeat)
                if id in self.callback_list:
                    self.callback_list[id](mission_heartbeat)
            else:
                self.log("Invalid checksum for mission heartbeat")
        if system_heartbeat is not None:
            if GroundStation._validate_checksum(system_heartbeat):
                with self.send_lock:
                    self.system_heartbeat = system_heartbeat
                id = GroundStation._get_msg_id(system_heartbeat)
                if id in self.callback_list:
                    self.callback_list[id](system_heartbeat)
            else:
                self.log("Invalid checksum for system heartbeat")

    @staticmethod
    def _validate_checksum(msg : str) -> bool:
        msg = msg.strip()
        # Remove the checksum (last 2 characters)
        og_checksum = msg[-2:]
        msg = msg[1:-3] # remove dollar sign, then, checksum and asterisk
        checksum = 0
        for char in msg:
            checksum ^= ord(char)
        checksum = hex(checksum)[2:]
        return og_checksum == checksum
    
if __name__ == "__main__":
    sample = "$RXPTH,031124,161229,ROBOT,R,1*47"
    print(GroundStation._validate_checksum(sample))
    print(GroundStation._get_msg_id(sample))

        
