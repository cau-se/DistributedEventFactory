from numpy import random
from distributed_event_factory.graph_builder.node import Node

class GraphBuilder:
    #ToDos: alle fixen parameter als eingaben hinzunehmen,temp_name_list mit einem name_provider ersetzen
    def __init__(self):
        self.probability_straight = 0.4
        self.probability_split = 0.3
        self.probability_join = 0.3
        self.max_length = 5
        self.active_children = []
        self.graph = {}
        self.temp_name_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","V","W","X","Y","Z","A1","B1","C1","D1","E1","F1","G1","H1","I1","J1","K1","L1","M1","N1","O1","P1","Q1","R1","S1","T1","U1","V1","W1","X1","Y1","Z1"]
        self.end_nodes = []

    def build_graph(self):
        self.active_children.append("start")
        self.graph["start"] = Node("start", 0, 1)
        possibilities = ["straight", "split", "join"]
        probabilities = [self.probability_straight, self.probability_split, self.probability_join]
        # print("TEST1:" + self.graph.__str__())
        # print("TEST2:" + self.graph["start"].__str__())

        while len(self.active_children) > 0:
            action = random.choice(possibilities, p=probabilities)
            match action:
                case "straight":
                    self.straight()
                case "split":
                    self.split()
                case "join":
                    self.join()
                case _:
                    print("Something went horribly wrong in the switch statement of the graph_builder")


        all_variations = 0
        for end_node in self.end_nodes:
            all_variations += self.graph[end_node].get_variations()

        return self.graph, all_variations


    #for now only splitting in 2 branches
    def split (self):
        active_node = self.active_children.pop(0)

        if self.graph[active_node].get_length() > self.max_length:
            print("Error: Graph too long")
        elif self.graph[active_node].get_length() == self.max_length:
            self.end_nodes.append(active_node)
        else:
            #in case of allowing more than 2 branches, just loop the spawn child the amount you want
            self.spawn_child([active_node])
            self.spawn_child([active_node])

    #for now only joins up to 2 nodes, by creating a node they are joining in, if possible
    def join(self):
        #to change the amount of allowed joins, just take number of joins as parameter
        number_of_joins = 2
        active_nodes = []

        while len(active_nodes) < number_of_joins and len(self.active_children) > 0:
            active_nodes.append(self.active_children.pop(0))
            if self.graph[active_nodes[len(active_nodes) - 1]].get_length() > self.max_length:
                print("Error: Graph too long")
            elif self.graph[active_nodes[len(active_nodes) - 1]].get_length() == self.max_length:
                self.end_nodes.append(active_nodes[len(active_nodes) - 1])
                active_nodes.pop()

        if len(active_nodes) < number_of_joins:
            active_nodes.reverse()
            for temp_node in active_nodes:
                self.active_children = [temp_node] + self.active_children
        else:
            self.spawn_child(active_nodes)



    def straight(self):
        active_node = self.active_children.pop(0)

        if self.graph[active_node].get_length() > self.max_length:
            print("Error: Graph too long")
        elif self.graph[active_node].get_length() == self.max_length:
            self.end_nodes.append(active_node)
        else:
            self.spawn_child([active_node])

    # takes a list of parents and adds a child to them
    def spawn_child(self, parent_list):
        new_name = self.temp_name_list.pop(0)
        current_variations = 0
        current_length = 0

        #finding current length and number of variations in case of join
        for parent in parent_list:
            self.graph[parent].add_child(new_name)
            current_variations += self.graph[parent].get_variations()
            temp_length = self.graph[parent].get_length()
            if temp_length > current_length:
                current_length = temp_length

        self.graph[new_name] = Node(new_name, current_length + 1, current_variations)
        self.active_children.append(new_name)