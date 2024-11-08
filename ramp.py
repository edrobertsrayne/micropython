import time
from enum import Enum
from easing import EasingFunction


class LoopMode(Enum):
    ONCE_FORWARD = 1
    LOOP_FORWARD = 2
    FORTH_AND_BACK = 3
    ONCE_BACKWARD = 4
    LOOP_BACKWARD = 5
    BACK_AND_FORTH = 6


class Ramp:
    def __init__(self):
        self._current_value = 0.0
        self._origin_value = 0.0
        self._target_value = 0.0
        self._start_time = 0
        self._duration = 0
        self._grain = 1.0
        self._is_running = False
        self._is_paused = False
        self._is_finished = True
        self._automation = True
        self._pause_start_time = 0
        self._pause_duration = 0
        self._loop_mode = LoopMode.ONCE_FORWARD
        self._cycle_count = 0
        self._reverse_direction = False
        self._easing_function = EasingFunction.linear

    def go(
        self,
        target_value,
        duration_ms,
        loop_mode=LoopMode.ONCE_FORWARD,
        easing_function=EasingFunction.linear,
    ):
        """Start a new interpolation towards target_value."""
        self._origin_value = self._current_value
        self._target_value = float(target_value)
        self._duration = duration_ms / 1000.0
        self._start_time = time.time()
        self._is_running = True
        self._is_finished = False
        self._is_paused = False
        self._pause_duration = 0
        self._loop_mode = loop_mode
        self._cycle_count = 0
        self._reverse_direction = loop_mode in [
            LoopMode.ONCE_BACKWARD,
            LoopMode.LOOP_BACKWARD,
        ]
        self._easing_function = easing_function
        return self

    def update(self):
        """Update interpolation value based on current time."""
        if not self._automation:
            return self

        if self._is_running and not self._is_paused:
            elapsed_time = time.time() - self._start_time - self._pause_duration

            if elapsed_time >= self._duration:
                if self._handle_cycle_completion():
                    self._current_value = (
                        self._target_value
                        if not self._reverse_direction
                        else self._origin_value
                    )
                    return self

                elapsed_time = 0

            # Calculate progress
            progress = elapsed_time / self._duration
            if self._reverse_direction:
                progress = 1 - progress

            # Apply easing function
            progress = self._easing_function(progress)

            # Linear interpolation
            delta = self._target_value - self._origin_value
            new_value = self._origin_value + (delta * progress)

            # Apply grain
            if self._grain > 0:
                new_value = round(new_value / self._grain) * self._grain

            self._current_value = new_value

        return self

    def pause(self):
        """Pause the interpolation."""
        if self._is_running and not self._is_paused:
            self._is_paused = True
            self._pause_start_time = time.time()
        return self

    def resume(self):
        """Resume from pause."""
        if self._is_paused:
            self._pause_duration += time.time() - self._pause_start_time
            self._is_paused = False
        return self

    def _handle_cycle_completion(self):
        """Handle completion of a single interpolation cycle based on loop mode."""
        if (
            self._loop_mode == LoopMode.ONCE_FORWARD
            or self._loop_mode == LoopMode.ONCE_BACKWARD
        ):
            self._is_running = False
            self._is_finished = True
            return True

        elif self._loop_mode in [LoopMode.FORTH_AND_BACK, LoopMode.BACK_AND_FORTH]:
            self._reverse_direction = not self._reverse_direction
            self._start_time = time.time() - self._pause_duration
            self._cycle_count += 1
            return False

        elif self._loop_mode in [LoopMode.LOOP_FORWARD, LoopMode.LOOP_BACKWARD]:
            self._start_time = time.time() - self._pause_duration
            self._cycle_count += 1
            return False

        return True

    def getValue(self):
        """Get current interpolation value."""
        return self._current_value

    def getOrigin(self):
        """Get starting value of current interpolation."""
        return self._origin_value

    def getTarget(self):
        """Get target value of current interpolation."""
        return self._target_value

    def getCompletion(self):
        """Get interpolation completion percentage."""
        if self._is_finished:
            return 100.0
        if not self._is_running:
            return 0.0

        elapsed_time = time.time() - self._start_time - self._pause_duration
        completion = (elapsed_time / self._duration) * 100
        if self._reverse_direction:
            completion = 100 - completion
        return min(100.0, max(0.0, completion))

    def getDuration(self):
        """Get interpolation duration in milliseconds."""
        return self._duration * 1000

    def setGrain(self, grain):
        """Set interpolation grain (step size)."""
        self._grain = float(grain)
        return self

    def setAutomation(self, auto):
        """Set automation mode."""
        self._automation = bool(auto)
        return self

    def isPaused(self):
        """Get pause state."""
        return self._is_paused

    def isRunning(self):
        """Get running state."""
        return self._is_running

    def isFinished(self):
        """Get finished state."""
        return self._is_finished

    def getCycleCount(self):
        """Get the number of completed cycles."""
        return self._cycle_count

    def getLoopMode(self):
        """Get current loop mode."""
        return self._loop_mode
