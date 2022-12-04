"""
Encoder library for Raspberry Pi for measuring quadrature encoded signals.
Concept created by Mivallion <mivallion@gmail.com>
Expanded on by T-Lind
"""

import RPi.GPIO as GPIO


class BaseEncoder:
    """
    Encoder class allows to work with rotary encoder
    which connected via two pin A and B.
    Works only on interrupts because all RPi pins allow that.
    This library is a simple port of the Arduino Encoder library
    (https://github.com/PaulStoffregen/Encoder)
    """

    def __init__(self, A, B):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A, GPIO.IN)
        GPIO.setup(B, GPIO.IN)
        self.A = A
        self.B = B
        self.pos = 0
        self.state = 0
        if GPIO.input(A):
            self.state |= 1
        if GPIO.input(B):
            self.state |= 2
        GPIO.add_event_detect(A, GPIO.BOTH, callback=self.__update)
        GPIO.add_event_detect(B, GPIO.BOTH, callback=self.__update)

    def __update(self, channel) -> None:
        """
        update() calling every time when value on A or B pins changes.
        It updates the current position based on previous and current states
        of the rotary encoder.
        """
        state = self.state & 3
        if GPIO.input(self.A):
            state |= 4
        if GPIO.input(self.B):
            state |= 8

        self.state = state >> 2

        if state == 1 or state == 7 or state == 8 or state == 14:
            self.pos += 1
        elif state == 2 or state == 4 or state == 11 or state == 13:
            self.pos -= 1
        elif state == 3 or state == 12:
            self.pos += 2
        elif state == 6 or state == 9:
            self.pos -= 2

    def read(self) -> int:
        """
        read() simply returns the current position of the rotary encoder.
        """
        return self.pos

    def write(self, pos=0) -> None:
        """
        write() sets the encoder to the position you specify, default is pos=0
        :param pos: position to set to
        """
        self.pos = pos
