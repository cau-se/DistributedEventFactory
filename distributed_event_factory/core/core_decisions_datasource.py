class GenericDecisions:
    def __init__(
            self,
            simulation_provider,
            input_objects,
            workstation,
            workforce,
            start,
            end
    ):
        self.simulation_provider = simulation_provider
        self.input_objects= input_objects
        self.workstation = workstation
        self.workforce = workforce
        self.start = start
        self.end = end

    def get_event_data(self):
        return self.simulation_provider.get_event_data()
    
    def get_input_data(self):
        return self.input_objects

    def get_workstation(self):
        return self.workstation

    def get_workforce(self):
        return self.workforce

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end