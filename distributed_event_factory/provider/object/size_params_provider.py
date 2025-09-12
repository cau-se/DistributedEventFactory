class SizeParamsProvider:
    def __init__(self, width:str, length:str, depth:str):
        self.width : float = float(width) if width else None
        self.length : float = float(length) if length else None
        self.depth : float = float(depth) if depth else None

    def __str__(self):
            return str({key: value for key, value in self.__dict__.items() if value})