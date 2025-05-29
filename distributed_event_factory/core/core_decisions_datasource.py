class GenericDecisions:
    def __init__(
            self,
            simulation_provider,
            type_parser
    ):
        self.simulation_provider = simulation_provider
        self.type_parser= type_parser

    def get_event_data(self):
        return self.simulation_provider.get_event_data()
    
    def get_input_data(self):
        return self.type_parser