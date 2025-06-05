class InputObjectProvider:
    def __init__(self, objectName, numberOfObject):
        self.objectName = objectName
        self.numberOfObject = numberOfObject

    def __str__(self):
        return str(self.__dict__)
