import time


class PIDController:
    def __init__(self, kp, ki, kd, setpoint, sample_time=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.sample_time = sample_time

        self.error = 0
        self.last_error = 0
        self.integral = 0
        self.derivative = 0
        self.output = 0

        self.last_time = time.time()

    def update(self, measured_value):
        now = time.time()
        dt = now - self.last_time

        if dt >= self.sample_time:
            # Calculate error
            self.error = self.setpoint - measured_value

            # Compute PID terms
            self.integral += self.error * dt
            self.derivative = (self.error - self.last_error) / dt

            # Calculate output
            self.output = (
                (self.kp * self.error)
                + (self.ki * self.integral)
                + (self.kd * self.derivative)
            )

            # Update last values
            self.last_error = self.error
            self.last_time = now

        return self.output
