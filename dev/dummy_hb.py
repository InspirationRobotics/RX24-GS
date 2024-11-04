import time
from ground_core import GroundStation

if __name__ == "__main__":
    gs = GroundStation("debug", 37564, dummy=True)
    while True:
        time.sleep(1)
        pass