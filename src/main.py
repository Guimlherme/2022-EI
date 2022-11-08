from perception import Sensors, State, Map
from decision_making import DecisionMaking

class Robot:
    def __init__(self, sensors, decision_making, world_map):
        self.sensors = sensors
        self.decision_making = decision_making
        self.state = State(world_map)
    
    def run(self):
        while True:
            perception = self.sensors.collect()
            self.state.update(perception)
            command = self.decision_making.decide(self.state, perception)
            command.execute()

world_map = Map()
sensors = Sensors(debug=True)
decision_making = DecisionMaking(debug=True)
robot = Robot(sensors, decision_making, world_map)

robot.run()
            