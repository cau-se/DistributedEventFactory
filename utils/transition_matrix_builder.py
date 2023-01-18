from typing import List


class TransitionMatrixBuilder:
    """
    A class for building transition matrices for Markov chains.
    """
    def __init__(self):
        """
        Initialize an empty transition matrix builder.
        """
        self.states = []
        self.transition_matrix = {}

    def add_state(self, state: str, p: float):
        """
         Add a new state to the transition matrix builder.

         :Args:
             state (str): The name of the new state.
             p (float): The probability of transitioning to itself.

         :returns:
             self
         """
        if state not in self.states:
            self.states.append(state)
            self.transition_matrix[state] = {}
            self.to(state,p=p)
        return self

    def to(self, next_state: str, p: float):
        """
        Add a transition from the current state to the next state with a given probability.

        Args:
            next_state (str): The name of the next state.
            p (float): The probability of transitioning to the next state.

        :returns:
            self
        """
        current_state = self.states[-1]
        self.transition_matrix[current_state][next_state] = p
        return self

    def to_matrix(self) -> List[List[float]]:
        """
        Convert the transition matrix to a 2D list of floats.

        :returns:
            List[List[float]]: The transition matrix as a 2D list of floats.
        """
        n: int = len(self.states)
        matrix: List[List[float]] = [[0 for _ in range(n)] for _ in range(n)]
        for i, state in enumerate(self.states):
            for j, next_state in enumerate(self.states):
                matrix[i][j] = self.transition_matrix[state].get(next_state, 0)
        return matrix

    def print_matrix(self):
        """
        Print the transition matrix in a human-readable format.
        """
        matrix = self.to_matrix()
        n = len(self.states)
        # find the max length of state names
        max_state_len = len(max(self.states, key=len))
        print(" " * (max_state_len + 1), *self.states)
        for i, state in enumerate(self.states):
            # padding spaces to align the columns
            print(f"{state:<{max_state_len}}  ", end="")
            for j in range(n):
                print(f"{matrix[i][j]:<{max_state_len}} ", end="")
            print()


builder = TransitionMatrixBuilder()
builder.add_state("state_a", p=0.9).to("state_b", p=0.1)
builder.add_state("state_b", p=0.7).to("state_a", p=0.3).to("state_d", p=0.1)
builder.add_state("state_c", p=0.5).to("state_a", p=0.5)
builder.add_state("state_d", p=0.0).to("state_c", p=0.5).to("state_b", p=0.5)

matrix = builder.to_matrix()
builder.print_matrix()
