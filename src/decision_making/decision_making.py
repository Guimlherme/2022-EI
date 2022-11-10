import numpy as np
from .astar import find_path

class DecisionMaking:
    def __init__(self, command_factory, debug=False):
        self.command_factory = command_factory
        self.debug = debug

    def decide(self, state, target, perception):
        if state.position_is(target):
            return self.command_factory.stopped()
# TODO: get target as node instead of coordinates
        next_waypoint = self.plan(state, target)
        print("Next waypoint: ", next_waypoint)

        if self.need_half_turn(state, next_waypoint):
            return self.command_factory.half_turn()

        # No half turn: just follow line towards waypoint
        if state.intersection_detected():
            return self.command_factory.forward(perception.line_angle)
        else:
            return self.command_factory.forward(perception.line_angle)
            
        return None

    def need_half_turn(self, state, waypoint):
        posR = np.array([state.x, state.y])
        posW = np.array(waypoint)
        v1 = np.array([np.cos(state.theta), np.sin(state.theta)])
        v2 = waypoint - posR
        product = np.dot(v1, v2)
        return product < 0

    def plan(self, state, target):
        path = find_path(state.world_map, state.node, target)
        next_waypoint = list(path)[1]
        return next_waypoint