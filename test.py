import unittest
from Test import TelemetryData

class TestTelemetryData(unittest.TestCase):

    def test_telemetry_data(self):
        telemetry_data = TelemetryData(1, 2, 3, 4, 5, 6, 7)
        self.assertEqual(telemetry_data.acc_x, 1)
        self.assertEqual(telemetry_data.acc_y, 2)
        self.assertEqual(telemetry_data.servo_x, 3)
        self.assertEqual(telemetry_data.servo_y, 4)
        self.assertEqual(telemetry_data.temperature, 5)
        self.assertEqual(telemetry_data.pressure, 6)
        self.assertEqual(telemetry_data.altitude, 7)


if __name__ == '__main__':
    unittest.main()