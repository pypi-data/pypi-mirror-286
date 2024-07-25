import smbus2
import time

# Define CAN baud rates
CAN_5KBPS = 1
CAN_10KBPS = 2
CAN_20KBPS = 3
CAN_25KBPS = 4
CAN_31K25BPS = 5
CAN_33KBPS = 6
CAN_40KBPS = 7
CAN_50KBPS = 8
CAN_80KBPS = 9
CAN_83K3BPS = 10
CAN_95KBPS = 11
CAN_100KBPS = 12
CAN_125KBPS = 13
CAN_200KBPS = 14
CAN_250KBPS = 15
CAN_500KBPS = 16
CAN_666KBPS = 17
CAN_1000KBPS = 18

CAN_OK = 0
CAN_MSGAVAIL = 1


class I2C_CAN:

    def __init__(self, address):
        self.IIC_ADDR = address
        self.m_ID = None
        self.m_RTR = None
        self.m_EXT = None
        self.bus = smbus2.SMBus(
            1
        )  # Assuming bus 1, this might be different on your system

    def make_checksum(self, data):
        return sum(data) & 0xFF

    def begin(self):
        self.IIC_CAN_SetReg(0x00, 0x01)  # Example: Reset command

    def IIC_CAN_SetReg(self, reg, data):
        if isinstance(data, list):
            self.bus.write_i2c_block_data(self.IIC_ADDR, reg, data)
        else:
            self.bus.write_byte_data(self.IIC_ADDR, reg, data)

    def IIC_CAN_GetReg(self, reg, length=1):
        if length == 1:
            return self.bus.read_byte_data(self.IIC_ADDR, reg)
        else:
            return self.bus.read_i2c_block_data(self.IIC_ADDR, reg, length)

    def begin_CAN(self, speedset):
        self.IIC_CAN_SetReg(0x01, speedset)  # Example: Set CAN speed
        return CAN_OK  # Simulate successful CAN initialization

    def init_mask(self, num, ext, ulData):
        data = [
            num,
            ext,
            ulData & 0xFF,
            (ulData >> 8) & 0xFF,
            (ulData >> 16) & 0xFF,
            (ulData >> 24) & 0xFF,
        ]
        self.IIC_CAN_SetReg(0x02, data)

    def init_filt(self, num, ext, ulData):
        data = [
            num,
            ext,
            ulData & 0xFF,
            (ulData >> 8) & 0xFF,
            (ulData >> 16) & 0xFF,
            (ulData >> 24) & 0xFF,
        ]
        self.IIC_CAN_SetReg(0x03, data)

    def send_msg_buf(self, id, ext, rtr, length, buf):
        data = [
            id & 0xFF,
            (id >> 8) & 0xFF,
            (id >> 16) & 0xFF,
            (id >> 24) & 0xFF,
            ext,
            rtr,
            length,
        ] + list(buf)
        self.IIC_CAN_SetReg(0x04, data)

    def read_msg_buf(self):
        length = self.IIC_CAN_GetReg(0x05)
        buf = self.IIC_CAN_GetReg(0x06, length)
        return length, buf

    def check_receive(self):
        return self.IIC_CAN_GetReg(0x0A)

    def check_error(self):
        return self.IIC_CAN_GetReg(0x0B)

    def get_can_id(self):
        id = self.IIC_CAN_GetReg(0x0C, 4)
        return id[0] | (id[1] << 8) | (id[2] << 16) | (id[3] << 24)

    def is_remote_request(self):
        return self.IIC_CAN_GetReg(0x0D)

    def is_extended_frame(self):
        return self.IIC_CAN_GetReg(0x0E)
