class Simulation():
    def __init__(self, environment, refresh_time):
        self.environment = environment
        self.time = 0
        self.agent = environment.agent
        self.dirty = environment.dirty
        self.refresh_time = refresh_time
    
    def start(self):
        pass 
