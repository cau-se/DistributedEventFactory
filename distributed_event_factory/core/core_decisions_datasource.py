class GenericDecisions:
    def __init__(
        self,
        simulation_provider,
        input_objects,
        workforce
    ):
        self.simulation_provider = simulation_provider
        self.input_objects = input_objects
        self.workforce = workforce

    def get_event_data(self):
        return self.simulation_provider.get_event_data()
    
    def get_input_data(self):
        return self.input_objects

    def get_workforce(self):
        return self.workforce
