class OutputObjectProvider:

    def __init__(self, objectName, numberOfObject, change, size):
        self.objectName = objectName
        #TODO hrei remove that ugly workaround
        self.object_type = objectName
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

    def __repr__(self):
        return self.__str__()
