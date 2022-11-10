import numpy as np
from .astar import find_path
import command
from math import pi, cos, sin, atan2
import scipy

from constants import ANGLE_THRESHOLD

class DecisionMaking:
    def __init__(self, command_factory, debug=False):
        self.command_factory = command_factory
        self.debug = debug
        self.current_state = StoppedState(command_factory)

    def decide(self, state, target, target_node, perception):
        next_waypoint = self.plan(state, target_node)
        print("Target: ", target_node)
        print("Next waypoint: ", next_waypoint)

        command = self.current_state.execute(state, target, next_waypoint, perception)
        next_state = self.current_state.check_transition(state, target, next_waypoint, perception)
        if next_state is not None:
            self.current_state = next_state
            
        if self.debug:
            print("Decision Making:", command.get_name())
        return command

    def need_half_turn(self, state, waypoint):
        posR = np.array([state.x, state.y])
        posW = np.array(waypoint)
        v1 = np.array([np.cos(state.theta), np.sin(state.theta)])
        v2 = waypoint - posR
        product = np.dot(v1, v2)
        return product < 0

    def plan(self, state, target_node):
        path = find_path(state.world_map, state.node, target_node)
        if path is None:
            return state.node
        path_list = list(path)
        if len(path_list) == 0:
            return state.node
        if len(path_list) == 1:
            return path_list[0]
        next_waypoint = path_list[1]
        return next_waypoint


class ForwardState:
    def __init__(self, command_factory):
        self.command_factory = command_factory
        self.next_waypoint = None
        self.next_waypoint_position = None

    def execute(self, state, target, next_waypoint, perception):
        if self.next_waypoint is None:
            self.next_waypoint = next_waypoint
            self.next_waypoint_position = np.array(state.world_map.nodes[next_waypoint])
        return self.command_factory.forward(perception.line_angle)

    def check_transition(self, state, target, next_waypoint, perception):
        changed_target = False
        if self.next_waypoint != next_waypoint:
            print("Changed waypoint!")
            changed_target = True
            self.next_waypoint = next_waypoint
            self.next_waypoint_position = np.array(state.world_map.nodes[next_waypoint])

        if state.position_is(target):
            return StoppedState(self.command_factory)

        robot_position = np.array([state.x, state.y])
        waypoint_vector = self.next_waypoint_position - robot_position
        waypoint_angle = atan2(waypoint_vector[1], waypoint_vector[0])

        angle_diference = angle_diference_with_sign(state.theta, waypoint_angle)
        print("Robot position: ", robot_position)
        print("Waypoint angle: ", waypoint_angle)
        print("Angle difference: ", angle_diference)

        # if changed to a target behind it, turn now
        if changed_target and (abs(angle_diference - pi) < ANGLE_THRESHOLD or abs(angle_diference + pi) < ANGLE_THRESHOLD):
            return TurnState(self.command_factory, state, angle_diference)
        # turn when arrive at an intersection
        elif state.intersection_detected() and abs(angle_diference) > ANGLE_THRESHOLD:
            return TurnState(self.command_factory, state, angle_diference)
        return None

class StoppedState:
    def __init__(self, command_factory):
        self.command_factory = command_factory
        
    def execute(self, state, target, target_node, perception):
        return self.command_factory.stopped()
        
    def check_transition(self, state, target, target_node, perception):
        if not state.position_is(target):
            return ForwardState(self.command_factory)
        return None

class TurnState:
    def __init__(self, command_factory, state, angle):
        self.angle = angle
        self.initial_theta = state.theta
        self.command_factory = command_factory

        self.finished_turning = False

    def execute(self, state, target, target_node, perception):
        return self.command_factory.turn(command.RIGHT)

    def check_transition(self, state, target, target_node, perception):
        if angle_diference(state.theta, self.initial_theta)  < np.deg2rad(10):
            self.finished_turning = True
        if self.finished_turning and not state.obstacle_detected:
            return ForwardState(self.command_factory)
        return None

def angle_diference(x, y):
    diff = y - x
    return min ( diff % (2*pi), (- diff) % (2*pi))


def angle_diference_with_sign(x, y):
    diff = y - x
    sign = get_direction(x, y)
    return sign * min ( diff % (2*pi), (- diff) % (2*pi))

def get_direction(x, y):
    x_v = np.array([cos(x), sin(x), 0])
    y_v = np.array([cos(y), sin(y), 0])
    prod = np.cross(x_v, y_v)
    return 1 if (prod[2] > 0) else -1

