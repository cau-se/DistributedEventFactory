class InputObjectProvider:
    def __init__(self, objectName, numberOfObject, lastState, size):
        self.objectName = objectName
        self.numberOfObject = numberOfObject
        self.lastState = lastState
        self.size = size

    def __str__(self):
        if self.lastState:
            return str(self.__dict__)
        return str({
            key: (str(value) if key == "size" else value)
            for key, value in self.__dict__.items()
            if value
        })
