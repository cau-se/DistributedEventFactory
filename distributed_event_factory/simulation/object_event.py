from process_mining_core.datastructure.core.event import Event


class ObjectEvent(Event):
    def __init__(self, timestamp, activity, node, group_id, input, output):
        Event.__init__(self, timestamp, activity, None, node, group_id)
        self.input = input
        self.output = output

    def getInput(self):
        return self.input

    def getOutput(self):
        return self.output

    def getDifference(self):
        return self.input + "->" + self.output

    def __str__(self):
        return str(self.__dict__)