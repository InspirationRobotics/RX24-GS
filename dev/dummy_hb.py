import time
from ground_core import GroundStation

if __name__ == "__main__":
    gs = GroundStation("0.0.0.0", 12345, dummy=True)
    while True:
        time.sleep(1)
        pass