class OutputObjectProvider:
    def __init__(self, objectName, numberOfObject, change):
        self.objectName = objectName
        self.numberOfObject = numberOfObject
        self.change = change

    def __str__(self):
        if self.change:
            return str(self.__dict__)
        else:
            return str({key: value for key, value in self.__dict__.items() if value})