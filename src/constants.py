import numpy as np

# Values used for real robot
CYCLE_TIME = 120e-3 # s
DISTANCE_THRESHOLD = 20 # cm

# Values used for simulation
# CYCLE_TIME = 30e-3 # s
# DISTANCE_THRESHOLD = 5 # cm

FINISH_TURN_ANGLE_THRESHOLD = np.deg2rad(5) 
TURN_ANGLE_THRESHOLD = np.deg2rad(35)

WHEEL_DIST = 15.2 # centimeters

ONE_LINE_MAP = False
MINIMUM_AREA = 600
DISTANCE_BETWEEN_LINES = 200

DEL_SPEED_DEL_PSI = 0.06
ROBOT_WIDTH = 0.152 # m
ROBOT_SPEED_MAX = 0.15 # m/s
WHEEL_RADIUS = 0.0325 # m
OMEGA_MAX = 9.50 # rad/s

# CONTROL LAW PARAMETERS
XI = 0.70
WN = 4.50      # rad/s
TAU = 0.615    # s
TD = CYCLE_TIME     # s - time of discretization

CONTROL_PARAMETERS = {
     'phi':{'k':(2*(TAU-TD)*(WN**2))/(4+TD*WN*(4*XI+TAU*WN)),
            'k-1':-(2*(TAU+TD)*(WN**2))/(4+TD*WN*(4*XI+TAU*WN))},
     'u':{'k-1':(4-TD*WN*(4*XI+TAU*WN))/(4+TD*WN*(4*XI+TAU*WN))},
}
