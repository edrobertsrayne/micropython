from machine import Pin, time_pulse_us
from utime import sleep_us


class HCSR04:
    """
    A class to interface with HC-SR04 ultrasonic distance sensor

    Args:
        trigger_pin (int): GPIO pin number for trigger
        echo_pin (int): GPIO pin number for echo
        echo_timeout_us (int): Timeout in microseconds for echo pulse
    """

    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=30000):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.echo_timeout_us = echo_timeout_us

        # Initialize trigger pin to low
        self.trigger.value(0)

    def distance_mm(self):
        """
        Get distance measurement in millimeters

        Returns:
            float: Distance in millimeters or -1 if measurement failed
        """
        # Trigger pulse
        self.trigger.value(0)
        sleep_us(5)
        self.trigger.value(1)
        sleep_us(10)
        self.trigger.value(0)

        # Wait for echo pulse and measure its duration
        duration = time_pulse_us(self.echo, 1, self.echo_timeout_us)

        # Return -1 if measurement failed (timeout)
        if duration < 0:
            return -1

        # Calculate distance in mm
        # Speed of sound is approximately 343.2 m/s or 0.3432 mm/microsecond
        # Distance = (duration * speed of sound) / 2 (round trip)
        distance = (duration * 0.3432) / 2

        return distance

    def distance_cm(self):
        """
        Get distance measurement in centimeters

        Returns:
            float: Distance in centimeters or -1 if measurement failed
        """
        mm = self.distance_mm()
        return -1 if mm == -1 else mm / 10
