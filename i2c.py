import errno
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

                try:
                    bus = SMBus(1)
                except FileNotFoundError as error:
                    logger.warning(
                        "I2C bus 1 is unavailable (%s); point changes will be local only",
                        error,
                    )
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
        try:
            self.bus.write_i2c_block_data(address, 0, [value])
        except OSError as error:
            # A missing/unresponsive I2C device commonly reports EIO,
            # ENXIO, or EREMOTEIO on Linux. Disable further I2C writes so
            # startup can continue without repeatedly logging the same issue.
            missing_device_errors = {
                errno.EIO,
                errno.ENXIO,
                getattr(errno, "EREMOTEIO", 121),
            }
            if error.errno not in missing_device_errors:
                raise

            logger.warning(
                "No I2C device responded at address 0x%02X (%s); "
                "point changes will be local only until the application restarts",
                address,
                error,
            )
            self.bus = None
