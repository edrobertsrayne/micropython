"""
TB6612FNG Single Motor Control Class for MicroPython
"""


class Motor:
    def __init__(self, in1, in2, pwm, stby, offset=0):
        """
        Initialize a single motor

        Args:
            in1 (Pin): First input pin
            in2 (Pin): Second input pin
            pwm (Pin): PWM control pin
            stby (Pin): Standby pin (can be shared between multiple motors)
            offset (float): Speed offset for motor calibration (0-1)
        """
        self.in1 = in1
        self.in2 = in2
        self.pwm = pwm
        self.stby = stby
        self.offset = offset

        # Initialize pins as outputs
        self.in1.init(self.in1.OUT)
        self.in2.init(self.in2.OUT)
        self.pwm.init(self.pwm.OUT)
        self.stby.init(self.stby.OUT)

        # Ensure motor starts in stopped state
        self.stop()

    def forward(self, speed):
        """
        Run motor forward at specified speed

        Args:
            speed (float): Motor speed from 0 to 1
        """
        self.in1.value(1)
        self.in2.value(0)
        self.pwm.value(int(speed * (1 - self.offset)))
        self.stby.value(1)

    def reverse(self, speed):
        """
        Run motor in reverse at specified speed

        Args:
            speed (float): Motor speed from 0 to 1
        """
        self.in1.value(0)
        self.in2.value(1)
        self.pwm.value(int(speed * (1 - self.offset)))
        self.stby.value(1)

    def stop(self):
        """Stop the motor"""
        self.in1.value(0)
        self.in2.value(0)
        self.pwm.value(0)
        self.stby.value(0)

    def brake(self):
        """
        Actively brake the motor (different from stop)
        by setting both inputs high
        """
        self.in1.value(1)
        self.in2.value(1)
        self.pwm.value(0)
        self.stby.value(1)
