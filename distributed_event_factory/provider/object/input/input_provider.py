class InputObjectProvider:
    def __init__(self, objectName, numberOfObject, lastState):
        self.objectName = objectName
        self.numberOfObject = numberOfObject
        self.lastState = lastState

    def __str__(self):
        return str(self.__dict__)
