from enum import Enum, auto
class signal:
    def __str__(self) -> str:
        return "generic_signal"

class traffic_light(signal):
    class state(Enum):
        GREEN = auto()
        RED = auto(),
        YELLOW = auto(),
        
    def __str__(self) -> str:
        return "traffic_light"

class priority(signal):
    def __str__(self) -> str:
        return "priority"

class stop(signal):
    def __str__(self) -> str:
        return "stop"

class yield_to(signal):
    def __str__(self) -> str:
        return "yield_to"

class speed_obligations(signal):
    def __str__(self) -> str:
        return "generic_speed_obligation"

class max_speed(speed_obligations):
    def __str__(self) -> str:
        return "max_speed"

class min_speed(speed_obligations):
    def __str__(self) -> str:
        return "min_speed"

class kepp_speed(speed_obligations):
    def __str__(self) -> str:
        return "keep_speed"

