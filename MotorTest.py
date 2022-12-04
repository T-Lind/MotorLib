import math
from time import time

from Motorlib import Motor, MotorType, RunMode

# Time to run the motor, in seconds
RUN_TIME = 10

# Number of periods
N_PERIODS = 2

# Define pwm and encoder pins
pwm = (3, 2)
encoder = (11, 12)

# Establish a motor object for a gobilda 312 RPM motor, with the specified pwm and encoder ports and position type control
my_motor = Motor(MotorType.GOBILDA_312, *pwm, *encoder, RunMode.POSITION_CONTROL)

# Set PID for the motor
my_motor.set_pid_coefficients(kP=0.001)

# Target position function to follow - sin wave of N_PERIODS over RUN_TIME length
target = lambda t: my_motor.type.TICKS_PER_REV * math.sin(N_PERIODS * math.pi * t / (RUN_TIME / 2))

before = time()
current = 0
while current < RUN_TIME:
    my_motor.set_target(target(current))
    my_motor.update_pid()
    current = time() - before

my_motor.stop()
