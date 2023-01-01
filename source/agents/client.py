from __future__ import annotations

class client:
    def __init__(self, location, destination, request_time) -> None:
        self.location = location
        self.destination = destination
        self.request_time = request_time
    
    def __gt__(self, other : client):
        return self.request_time > other.request_time
    
    def __lt__(self, other : client):
        return self.request_time < other.request_time
    
    def __ge__(self, other : client):
        return self.request_time >= other.request_time
    
    def __le__(self, other : client):
        return self.request_time <= other.request_time