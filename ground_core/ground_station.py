import time
from typing import Tuple
from threading import Thread, Lock
from comms_core import Client, Logger, CustomSocketMessage as csm
from .heartbeat import SystemHeartbeat, MissionHeartbeat

'''
A pretty simple class that receives a heartbeat from the server, stores it, and then sends it to a 
separate judges server at 1hz. We can add callbacks to run based off the message id.
'''

class GroundStation(Logger):

    def __init__(self, TD_IP, TD_port, *, debug=False, dummy=False) -> None:
        super().__init__("GroundStation")
        self.dummy = dummy
        if not dummy:
            self.boat_client = Client("192.168.3.2", callback=self._boat_callback)
            self.boat_client.start()
        if not debug:
            self.TD_client = Client(TD_IP, port=TD_port, TD=True, callback=self.TD_callback)

        self.mission_heartbeat = None
        self.system_heartbeat = None
        self.mi_flag = True
        self.sy_flag = True
        self.callback_list = {}

        self.active = True
        self.send_thread = Thread(target=self._send_heartbeat)
        self.send_lock = Lock()
        if not debug:
            self.TD_client.start()
            self.send_thread.start()
        
    def TD_callback(self, msg : str, address : Tuple[str, int]):
        if self.mission_heartbeat:
            if self.mission_heartbeat in msg:
                self.mission_heartbeat = None
                self.mi_flag = True
        if self.system_heartbeat:
            if self.system_heartbeat in msg:
                self.system_heartbeat = None
                self.sy_flag = True

    def add_callback(self, msg_id, callback):
        self.callback_list[msg_id] = callback

    def __del__(self):
        self.active = False
        self.send_thread.join()
        self.boat_client.stop()
        if not self.debug:
            self.TD_client.stop()

    @staticmethod
    def _get_msg_id(msg : str) -> str:
        return msg.split(",")[0][1:]
    
    def _send_heartbeat(self):
        while self.active:
            with self.send_lock:
                if self.dummy:
                    self.mission_heartbeat = str(MissionHeartbeat(["RXCOD", "RBG"]))
                    self.system_heartbeat = str(SystemHeartbeat((42.0, -71.0), "1"))

                if self.system_heartbeat is not None and self.sy_flag:
                    self.TD_client.send(self.system_heartbeat)
                    self.sy_flag = False

                time.sleep(0.5)

                if self.mission_heartbeat is not None and self.mi_flag:
                    self.TD_client.send(self.mission_heartbeat)
                    self.mi_flag = False

            time.sleep(0.5)

    def _boat_callback(self, msg : str, address : Tuple[str, int]):
        data = csm.decode(msg)
        if data is None:
            return
        mission_heartbeat = data.get("mission")
        system_heartbeat = data.get("system")
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
        # Remove the checksum (characters after the asterisk)
        cs_pos = msg.rfind("*")
        og_checksum = msg[cs_pos + 1:]
        msg = msg[1:cs_pos] # remove dollar sign, then, checksum and asterisk
        checksum = 0
        for char in msg:
            checksum ^= ord(char)
        checksum = hex(checksum)[2:]
        return og_checksum == checksum
    
if __name__ == "__main__":
    sample = "$RXPTH,031124,161229,ROBOT,R,1*47"
    print(GroundStation._validate_checksum(sample))
    print(GroundStation._get_msg_id(sample))

        
