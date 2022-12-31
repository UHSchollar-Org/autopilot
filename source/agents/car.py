from source.environment.map import *
from source.agents.pilot import pilot


class car:
    """
    """
    def __init__(self, _pilot : pilot) -> None:
        """Initialization of the CAR class

        Args:
            _pilot (pilot): Pilot is in charge of driving the car and establishing the route
        """
        self.taximeter = 0
        self.odometer = 0
        self.pilot = _pilot
        
    def move(self) -> None:
        """Move the car according to the route given by the pilot
        """
        self.pilot.drive_next_loc()
