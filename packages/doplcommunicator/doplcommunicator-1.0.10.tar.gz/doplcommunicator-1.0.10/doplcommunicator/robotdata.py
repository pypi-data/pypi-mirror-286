class RobotData():
    def __init__(self, enabled: bool, x: float, y: float, z: float):
        self.enabled = enabled
        self.pressure = Pressure(x, y, z)

    @classmethod
    def fromDict(self, robot_data):
        return RobotData(robot_data["enabled"], robot_data["pressure"]["x"], robot_data["pressure"]["y"], robot_data["pressure"]["z"])

    def toDict(self):
        return {
            "enabled": self.enabled,
            "pressure": self.pressure.toDict(),
        }

    def __eq__(self, other): 
        if not isinstance(other, RobotData):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return self.enabled == other.enabled and \
            self.pressure == other.pressure
    
class Pressure:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def toDict(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

    def __eq__(self, other): 
        if not isinstance(other, Pressure):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and \
            self.y == other.y and \
            self.z == other.z
