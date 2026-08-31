try:
    import smbus
except ImportError:
    print("smbus not found, i2c disabled")
    smbus = None


class i2c_control:
    def __init__(self):
        self.no_smbus = False
        if smbus:            
            self.bus = smbus.SMBus(1)
        else:
            self.no_smbus = True

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
        print("Sending Messsage " + bin(value) + " to address " + bin(address))
        print([value])
        if self.no_smbus:
            print("No smbus, I2C Disabled")
        try:
            self.bus.write_i2c_block_data(address, 0, [value])
        except:
            print("I2C Command Failed")
