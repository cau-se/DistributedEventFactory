import numpy as np

import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import io

class MarkovChain:
    states: List[str]
    transition_matrix: List[List[float]]
    num_states: int

    def __init__(self, transition_matrix: List[List[float]], states: List[str]):
        """
        Initialize the MarkovChain instance.
        transition_matrix: matrix of transition probabilities, where entry (i, j) is the probability
                           of transitioning from state i to state j.
        states: list of states.
        """
        self.transition_matrix = np.array(transition_matrix)
        self.states = states
        self.num_states = len(states)

    def next_state(self, current_state: int) -> int:
        """
        Returns the index of the next state.
        current_state: index of the current state.
        """
        return np.random.choice(self.num_states, p=self.transition_matrix[current_state, :])

    def simulate(self, current_state: int, num_steps: int) -> List[str]:
        """
        Simulate the Markov chain for num_steps steps.
        current_state: index of the current state.
        num_steps: number of steps to simulate.
        """
        states_simulated = [current_state]
        for i in range(num_steps):
            next_state = self.next_state(states_simulated[-1])
            states_simulated.append(next_state)
        return [self.states[i] for i in states_simulated]

    def steady_state(self) -> List[float]:
        """
        Compute the steady-state probabilities of the Markov chain to understand the long-term behavior.
        """

        # An Eigenvector is a vector whose direction remains unchanged when a linear transformation is applied to it.
        eigen_values, eigen_vectors = np.linalg.eig(self.transition_matrix.T)
        steady_state = eigen_vectors[:, np.isclose(eigen_values, 1)].flatten().real
        steady_state /= steady_state.sum()
        return steady_state

    def transition_probability(self, state1: str, state2: str) -> float:
        """
        Compute the probability of transitioning from state1 to state2
        """
        i, j = self.states.index(state1), self.states.index(state2)
        return self.transition_matrix[i, j]

    def all_edges(self) -> List[Tuple[str, str, float]]:
        """
        Returns all possible edges in the Markov Chain
        """
        edges = []
        for i in range(self.num_states):
            for j in range(self.num_states):
                if self.transition_matrix[i, j] > 0:
                    edges.append((self.states[i], self.states[j], self.transition_matrix[i, j]))
        return edges

    def visualize(self):
        """
        Visualize the Markov Chain
        """
        di_graph: nx.DiGraph = nx.DiGraph()
        for i in range(self.num_states):
            di_graph.add_node(self.states[i])

        for a, b, w in self.all_edges():
            di_graph.add_edge(a, b, weight=w)

        pos: dict = nx.circular_layout(di_graph)

        nx.draw_networkx_nodes(di_graph, pos)
        nx.draw_networkx_edges(di_graph, pos, arrowsize=15, arrowstyle='->', connectionstyle='arc3,rad=0.1')
        nx.draw_networkx_labels(di_graph, pos)

        edge_labels: dict[tuple[str, str], float] = {
            (i, j): round(self.transition_matrix[self.states.index(i)][self.states.index(j)], 2)
            for i, j in di_graph.edges()
        }

        nx.draw_networkx_edge_labels(di_graph, pos, edge_labels=edge_labels, label_pos=0.35, font_size=8)
        plt.show()