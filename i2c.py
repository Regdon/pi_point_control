import logging
import os


logger = logging.getLogger(__name__)


class i2c_control:
    def __init__(self, bus=None):
        if bus is None:
            if os.name == "nt":
                logger.warning(
                    "I2C is unavailable on Windows; point changes will be local only"
                )
            else:
                try:
                    from smbus2 import SMBus
                except ModuleNotFoundError as error:
                    if error.name != "smbus2":
                        raise
                    from smbus import SMBus

                bus = SMBus(1)
        self.bus = bus

    def SendState(self, node, point, state):
        #node = 0,1,2,3
        #point = 0,1,2,3,4,5,6,7
        #state = 0,1

        pointBits = int(point)
        nodeBits = int(node)
        stateBits = int(state)

        #Format = binary bits [state][node][point]
        nodeBits = nodeBits << 4
        stateBits = stateBits << 6

        msg = stateBits + nodeBits + pointBits
        address = nodeBits

        self.write_to_arduino(address, msg)

    def write_to_arduino(self, address, value):
        if self.bus is None:
            return

        print("Sending Messsage " + bin(value) + " to address " + bin(address))
        print([value])
        self.bus.write_i2c_block_data(address, 0, [value])
