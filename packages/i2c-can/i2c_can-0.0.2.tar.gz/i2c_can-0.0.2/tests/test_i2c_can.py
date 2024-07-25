import unittest
from i2c_can import I2C_CAN, CAN_500KBPS, CAN_OK


class TestI2C_CAN(unittest.TestCase):

    def setUp(self):
        self.i2c_can = I2C_CAN(0x25)

    def test_initialization(self):
        result = self.i2c_can.begin_CAN(CAN_500KBPS)
        self.assertEqual(result, CAN_OK)

    def test_send_msg_buf(self):
        self.i2c_can.send_msg_buf(0x01, 0, 0, 8, [1, 2, 3, 4, 5, 6, 7, 8])
        # You would typically have more assertions here to verify the behavior


if __name__ == "__main__":
    unittest.main()
