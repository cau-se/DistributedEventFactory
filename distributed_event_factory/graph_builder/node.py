class Node:
    def __init__(self, name, length, variations):
        self.name = name
        self.current_length = length
        self.current_variations = variations
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_length(self):
        return self.current_length

    def get_variations(self):
        return self.current_variations

    def get_children(self):
        return self.children

    def get_name(self):
        return self.name

    def __str__(self):
        return "[name:" + self.name + ", current length: " + str(self.current_length) + ", current_variations: " + str(self.current_variations) + ", Children: " + self.children.__str__() + "]"