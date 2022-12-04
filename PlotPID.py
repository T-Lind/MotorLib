import math
import random

import matplotlib.pyplot as plt

from Motorlib import PIDController

SIM_TIME = 10
RESOLUTION = 0.01

data_tracking = []
target_tracking = []
time_tracking = []

target = lambda t: 10 * math.sin(t) + random.random() - 0.5 + (1 / 10) * t ** 2 - (math.e ** t / 1000)
pid = PIDController(0.3, 0, -2e-3, current_time=0)

pos = 10
t = 0
while t < SIM_TIME:
    target_pos = target(t)
    pos += pid.update(pos, set_point=target_pos, current_time=t)
    data_tracking.append(pos)
    target_tracking.append(target_pos)

    time_tracking.append(pid.get_current_time())
    t += RESOLUTION

plt.plot(time_tracking, data_tracking, color="blue")
plt.plot(time_tracking, target_tracking, color="red", alpha=0.6)
plt.show()
