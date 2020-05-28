import sys

from Simulator import Simulator
import numpy as np
np.set_printoptions(precision=4, suppress=True)

world_setup = 0
if len(sys.argv) - 1 > 0:
    world_setup = int(sys.argv[1])

sim = Simulator(world_setup)

sim.run()

