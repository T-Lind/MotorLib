from time import time

from RPi.GPIO import GPIO

from Motorlib import PIDController
from Motorlib.BaseEncoder import BaseEncoder
from Motorlib.MotorType import MotorType


class RunMode:
    POSITION_CONTROL = "0x_position"
    VELOCITY_CONTROL = "0x_velocity"
    RAW_POWER = "0x_raw_power"


class Motor:
    def __init__(self, type: MotorType, pwm_a: int, pwm_b, enc_a: int, enc_b: int, runMode=RunMode.VELOCITY_CONTROL):
        self.type = type
        self.__encoder = BaseEncoder(enc_a, enc_b)
        self.runMode = runMode

        self.__pwm = GPIO.PWM(pwm_a, pwm_b)

        self.__prev_time = None
        self.__prev_pos = None

        self.__pid = PIDController()

        self.__current_power = 0

    """
    PID functions to get and set the local PID object
    """

    def set_pid_coefficients(self, kP=0, kI=0, kD=0) -> None:
        self.__pid.set_kP(kP)
        self.__pid.set_kI(kI)
        self.__pid.set_kD(kD)

    def set_target(self, target: float) -> None:
        self.__pid.set_setpoint(target)

    def update_pid(self) -> None:
        if self.runMode == RunMode.VELOCITY_CONTROL:
            self.__current_power += self.__pid.update(self.get_angular_velocity())
        elif self.runMode == RunMode.POSITION_CONTROL:
            self.__current_power += self.__pid.update(self.__encoder.read())
        elif self.runMode == RunMode.RAW_POWER:
            # Cannot update PID using raw power!
            pass
        self.set_power(self.__current_power)


    """
    Get and set methods to determine what the motor's current position and velocity is at
    """

    def get_angle(self) -> float:
        return self.__encoder.read() / self.type.TICKS_PER_REV

    def get_angular_velocity(self) -> float:
        velocity = 0
        current_time = time()
        current_pos = self.__encoder.read()
        if not (self.__prev_time is None and self.__prev_pos is None):
            velocity = (current_pos - self.__prev_pos) / (current_time - self.__prev_time)
        self.__prev_time = current_time
        self.__prev_pos = current_pos
        return velocity

    def set_angle(self, angle) -> None:
        self.__encoder.write(pos=angle * self.type.TICKS_PER_REV)

    def set_power(self, power=None) -> None:
        power = self.__current_power if power is None else power
        self.__pwm.ChangeDutyCycle(self.__duty_cycle(self.__make_pulse(power)))

    def stop(self) -> None:
        self.__pwm.ChangeDutyCycle(0)

    """
    Private methods to convert power to a duty cycle
    """

    def __make_pulse(self, power) -> int:
        if power > 0:
            abs(power)
            return 990 * power + 1490
        elif power < 0:
            return 990 * power + 1510
        else:
            return 1500

    def __duty_cycle(self, pulse_width) -> float:
        return pulse_width / 1E6 * 400 * 100
