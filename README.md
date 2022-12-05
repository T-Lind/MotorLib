# MotorLib: A configurable library for 12V DC Motors
### Author: Tiernan Lindauer

MotorLib is for use with any microcontroller/computer that has GPIO, like the popular Raspberry Pi or Arduino boards.
It also requires the use of a PWM motor controller, with examples provided below.
Examples have been provided on how to use this library are provided in the `MotorTest.py` and `PlotPID.py` files.
`MotorTest.py` is also reproduced below:

```python
import math
from time import time

from pymotorlib import Motor, MotorType, RunMode
from pymotorlib.PWMDriver import GoBildaControl

# Time to run the motor, in seconds
RUN_TIME = 10

# Number of periods
N_PERIODS = 2

# Define pwm and encoder pins
pwm = 12
encoder = (11, 12)

# Establish a motor object for a gobilda 312 RPM motor, with the specified pwm and encoder ports and position type control
my_motor = Motor(MotorType.GOBILDA_312, pwm, *encoder, GoBildaControl, RunMode.POSITION_CONTROL)

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
```

As you can see, it is relatively easy to get your motor up and running with this library. Here are the different config options available:

### Motor Configuration

##### Motor type (What motor you're running):

[ORIBITAL_20](https://www.andymark.com/products/neverest-orbital-20-gearmotor), [GOBILDA_312](https://www.gobilda.com/5203-series-yellow-jacket-planetary-gear-motor-19-2-1-ratio-24mm-length-8mm-rex-shaft-312-rpm-3-3-5v-encoder/) - you can add more by creating a class that has a static `TICKS_PER_REV` variable

Example:
```python
class NEW_MOTOR:
    TICKS_PER_REV = 500  # Use your own value here for the amount of encoder ticks for each revolution
```

##### Set the GPIO pins:
The PWM channel should be set to the pin the PWM wire is connected to. The encoder pins should correspond first to channel A, second to channel B.

##### RunMode (how to use the motor):
`POSITION_CONTROL` - go to a position using PID, `VELOCITY_CONTROL` - go to a velocity using PID, `RAW_POWER` - do not use PID, instead just set the power manually

##### Using a custom motor controller:
By default, it is assumed you are using the [GoBilda Motor Controller](https://www.gobilda.com/1x15a-motor-controller-30a-peak/). There is also support for the [REV Robotics Spark Mini](https://www.revrobotics.com/rev-31-1230/).
The example uses `GoBildaControl`, however if you switch that to `SparkMini` you can run the motor off the Spark Mini as well.

To use your own custom PWM controller, set a class up as follows:
```python
class NewController(PWMDriver):
    MIN_PULSE = 300  # Set this to whatever your controller's min pulse width is
    MAX_PULSE = 2300  # Set this to whatever your controller's max pulse width is  
    half_width = (MAX_PULSE - MIN_PULSE) / 2

    @staticmethod
    def make_pulse(power):
        return (power * NewController.half_width) + NewController.MIN_PULSE + NewController.half_width
```
`MIN_PULSE` should be equivalent to a power of `-1`. `MAX_PULSE` should equate to a power of `1`.

##### Bugs/Issues
To report an issue or bug in the code, please start one [here](https://github.com/T-Lind/MotorLib/issues) on GitHub!

###
T. Lindauer
