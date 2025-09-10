class InputObjectProvider:
    def __init__(self, objectName, numberOfObject, lastState):
        self.objectName = objectName
        self.numberOfObject = numberOfObject
        self.lastState = lastState

    def __str__(self):
        if self.lastState:
            return str(self.__dict__)
        else:
            return str({key: value for key, value in self.__dict__.items() if value})
