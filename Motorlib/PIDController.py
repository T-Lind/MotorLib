from time import time


class PIDController:
    """
    PID Controller
    """

    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):

        self.__kP = P
        self.__kI = I
        self.__kD = D

        self.__sample_time = 0.00
        self.__current_time = current_time if current_time is not None else time()
        self.__last_time = self.__current_time

        self.__set_point = 0.0

        self.__p_term = 0.0
        self.__i_term = 0.0
        self.__d_term = 0.0
        self.__last_error = 0.0

        # Windup Guard
        self.__int_error = 0.0
        self.__windup_guard = 20.0

        self.__output = 0.0

    def clear(self) -> None:
        """
        Clears PID computations and coefficients
        """
        self.__set_point = 0.0

        self.__p_term = 0.0
        self.__i_term = 0.0
        self.__d_term = 0.0
        self.__last_error = 0.0

        # Windup Guard
        self.__int_error = 0.0
        self.__windup_guard = 20.0

        self.__output = 0.0

    def update(self, feedback_value, set_point=None, current_time=None) -> float:
        """
        Calculates PID value for given reference feedback, returns the adjustment to make
        Can pass time to not use the time since the epoch
        """

        self.__set_point = set_point if set_point is not None else self.__set_point

        error = self.__set_point - feedback_value

        self.__current_time = current_time if current_time is not None else time()
        delta_time = self.__current_time - self.__last_time
        delta_error = error - self.__last_error

        if delta_time >= self.__sample_time:
            self.__p_term = self.__kP * error
            self.__i_term += error * delta_time

            if self.__i_term < -self.__windup_guard:
                self.__i_term = -self.__windup_guard
            elif self.__i_term > self.__windup_guard:
                self.__i_term = self.__windup_guard

            self.__d_term = 0.0
            if delta_time > 0:
                self.__d_term = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.__last_time = self.__current_time
            self.__last_error = error

            self.__output = self.__p_term + (self.__kI * self.__i_term) + (self.__kD * self.__d_term)
        return self.__output

    def get_current_time(self) -> float:
        return self.__current_time

    def set_setpoint(self, new_setpoint) -> None:
        self.__set_point = new_setpoint

    def set_kP(self, proportional_gain) -> None:
        """
        Determines how aggressively the PID reacts to the current error with setting Proportional Gain
        """
        self.__kP = proportional_gain

    def set_kI(self, integral_gain) -> None:
        """
        Determines how aggressively the PID reacts to the current error with setting Integral Gain
        """
        self.__kI = integral_gain

    def set_kD(self, derivative_gain) -> None:
        """
        Determines how aggressively the PID reacts to the current error with setting Derivative Gain
        """
        self.__kD = derivative_gain

    def setWindup(self, windup) -> None:
        """
        Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.__windup_guard = windup

    def setSampleTime(self, sample_time) -> None:
        """
        PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.__sample_time = sample_time
