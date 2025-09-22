class OutputObjectProvider:

    def __init__(self, objectName, numberOfObject, change, size):
        self.objectName = objectName
        self.numberOfObject = numberOfObject
        self.change = change
        self.size = size

    def __str__(self):
        if self.change:
            return str(self.__dict__)
        return str({
            key: (str(value) if key == "size" else value)
            for key, value in self.__dict__.items()
            if value
        })