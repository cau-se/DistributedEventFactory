class InputWorkforceProvider:
    def __init__(self, name, numberOfWorkforce):
        self.name = name
        self.numberOfWorkforce = numberOfWorkforce

class WorkforceStartPositionProvider(InputWorkforceProvider):
    def __init__(self, name, location, numberOfWorkforce):
        InputWorkforceProvider.__init__(self, name, numberOfWorkforce)
        self.location = location
