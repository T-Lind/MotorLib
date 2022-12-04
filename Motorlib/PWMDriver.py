# Father class - do not use!
import abc


class PWMDriver:
    MIN_PULSE, MAX_PULSE = 0, 0
    half_width = (MAX_PULSE - MIN_PULSE) / 2

    @staticmethod
    @abc.abstractmethod
    def make_pulse(power) -> float:
        pass


# Example controllers:

class SparkMini(PWMDriver):
    MIN_PULSE = 500
    MAX_PULSE = 2500
    half_width = (MAX_PULSE - MIN_PULSE) / 2

    @staticmethod
    def make_pulse(power):
        return (power * SparkMini.half_width) + SparkMini.MIN_PULSE + SparkMini.half_width


class GoBildaControl(PWMDriver):
    MIN_PULSE = 1050
    MAX_PULSE = 1950
    half_width = (MAX_PULSE - MIN_PULSE) / 2

    @staticmethod
    def make_pulse(power):
        return (power * GoBildaControl.half_width) + GoBildaControl.MIN_PULSE + GoBildaControl.half_width
