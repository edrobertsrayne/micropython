from time import sleep


class MPU6050:
    # MPU6050 Registers and their Address
    _SMPLRT_DIV = 0x19
    _CONFIG = 0x1A
    _GYRO_CONFIG = 0x1B
    _ACCEL_CONFIG = 0x1C
    _INT_ENABLE = 0x38
    _ACCEL_XOUT_H = 0x3B
    _ACCEL_YOUT_H = 0x3D
    _ACCEL_ZOUT_H = 0x3F
    _GYRO_XOUT_H = 0x43
    _GYRO_YOUT_H = 0x45
    _GYRO_ZOUT_H = 0x47
    _PWR_MGMT_1 = 0x6B
    _WHO_AM_I = 0x75

    def __init__(self, i2c, addr=0x68):
        """Initialize MPU6050.

        Args:
            i2c: initialized I2C object
            addr: I2C address of MPU6050 (default: 0x68)
        """
        self.i2c = i2c
        self.addr = addr

        # Calibration offsets
        self._gyro_offset = {"x": 0, "y": 0, "z": 0}
        self._accel_offset = {"x": 0, "y": 0, "z": 0}

        # Wake up the MPU6050
        self._wake()

        # Check if sensor is ready
        if self._read_byte(self._WHO_AM_I) != 0x68:
            raise OSError("MPU6050 not found!")

        # Configure the sensor
        self._configure()

    def _write_byte(self, reg, val):
        """Write a single byte to a register."""
        self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def _read_byte(self, reg):
        """Read a single byte from a register."""
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def _read_word(self, reg):
        """Read a word from register."""
        high = self._read_byte(reg)
        low = self._read_byte(reg + 1)
        value = (high << 8) + low

        # Convert to signed value
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value

    def _wake(self):
        """Wake up the sensor."""
        self._write_byte(self._PWR_MGMT_1, 0)

    def _configure(self):
        """Configure the sensor's settings."""
        # Sample rate divider
        self._write_byte(self._SMPLRT_DIV, 0x07)
        # Set gyroscope full scale range
        # Range selects ±250 degrees/s
        self._write_byte(self._GYRO_CONFIG, 0)
        # Set accelerometer full scale range
        # Range selects ±2g
        self._write_byte(self._ACCEL_CONFIG, 0)

    def calibrate(self, samples=100, delay_ms=5):
        """Calibrate the sensor by calculating offset values.

        Place the sensor on a flat, stable surface and keep it still during calibration.

        Args:
            samples (int): Number of samples to take for calibration
            delay_ms (int): Delay between samples in milliseconds

        Returns:
            dict: Calibration results with current offset values
        """
        print("Calibrating MPU6050... Keep the sensor still!")

        # Reset calibration offsets
        self._gyro_offset = {"x": 0, "y": 0, "z": 0}
        self._accel_offset = {"x": 0, "y": 0, "z": 0}

        # Initialize variables for averaging
        gyro_sums = {"x": 0, "y": 0, "z": 0}
        accel_sums = {"x": 0, "y": 0, "z": 0}

        # Collect samples
        for _ in range(samples):
            # Read raw values
            ax, ay, az = self.acceleration
            gx, gy, gz = self.gyroscope

            # Accumulate values
            gyro_sums["x"] += gx
            gyro_sums["y"] += gy
            gyro_sums["z"] += gz

            accel_sums["x"] += ax
            accel_sums["y"] += ay
            accel_sums["z"] += az

            sleep(delay_ms / 1000)

        # Calculate average offsets
        self._gyro_offset = {
            "x": gyro_sums["x"] / samples,
            "y": gyro_sums["y"] / samples,
            "z": gyro_sums["z"] / samples,
        }
        self._accel_offset = {
            "x": accel_sums["x"] / samples,
            "y": accel_sums["y"] / samples,
            "z": accel_sums["z"] / samples,
        }

        return {"gyro_offset": self._gyro_offset, "accel_offset": self._accel_offset}

    @property
    def acceleration(self):
        """Get calibrated accelerometer data in g's.

        Returns:
            tuple: Calibrated acceleration in g's (ax, ay, az)
        """
        ax = self._read_word(self._ACCEL_XOUT_H) / 16384.0 - self._accel_offset["x"]
        ay = self._read_word(self._ACCEL_YOUT_H) / 16384.0 - self._accel_offset["y"]
        az = self._read_word(self._ACCEL_ZOUT_H) / 16384.0 - self._accel_offset["z"]
        return (ax, ay, az)

    @property
    def gyroscope(self):
        """Get calibrated gyroscope data in degrees/s.

        Returns:
            tuple: Calibrated angular velocity in degrees/s (gx, gy, gz)
        """
        gx = self._read_word(self._GYRO_XOUT_H) / 131.0 - self._gyro_offset["x"]
        gy = self._read_word(self._GYRO_YOUT_H) / 131.0 - self._gyro_offset["y"]
        gz = self._read_word(self._GYRO_ZOUT_H) / 131.0 - self._gyro_offset["z"]
        return (gx, gy, gz)

    @property
    def temperature(self):
        """Get temperature in degrees Celsius.

        Returns:
            float: Temperature in degrees Celsius
        """
        raw_temp = self._read_word(self._ACCEL_XOUT_H + 8)
        return (raw_temp / 340.0) + 36.53

    @property
    def values(self):
        """Get all calibrated sensor data in a single dictionary.

        Returns:
            dict: Dictionary containing calibrated acceleration (g), gyroscope (degrees/s),
                 and temperature (Celsius) data
        """
        ax, ay, az = self.acceleration
        gx, gy, gz = self.gyroscope
        temp = self.temperature

        return {
            "acceleration": {"x": ax, "y": ay, "z": az},
            "gyroscope": {"x": gx, "y": gy, "z": gz},
            "temperature": temp,
        }
