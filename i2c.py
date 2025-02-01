import smbus

class i2c_control:
    def __init__(self):
        self.bus = smbus.SMBus(1)

    def SendState(self, node, point, state):
        #node = 0,1,2,3
        #point = 0,1,2,3,4,5,6,7
        #state = 0,1

        #Format = binary bits [state][node][point]
        pointBits = point
        nodeBits = node << 4
        stateBits = state << 6

        msg = stateBits + nodeBits + pointBits
        address = node

        self.write_to_arduino(address, msg)

    def write_to_arduino(self, address, value):
        print("Sending Messsage " + bin(value) + " to address " + bin(address))
        self.bus.write_i2c_block_data(address, 0, value)
