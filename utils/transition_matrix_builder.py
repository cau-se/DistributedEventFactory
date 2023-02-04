from typing import List

from utils.utils_types import BgColors, print_color


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
        self.duration_matrix = {}

    def add_state(self, state: str, p: float, t: float | tuple[float, float] = 1.0):
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
            self.duration_matrix[state] = {}
            self.to(state, p=p, t=t)
        return self

    def to(self, next_state: str, p: float, t: float | tuple[float, float] = 1.0):
        """
        Add a transition from the current state to the next state with a given probability.

        Args:
            next_state (str): The name of the next state.
            p (float): The probability of transitioning to the next state.
            t float | tuple[float, float]: the duration of the transition

        :returns:
            self
        """
        current_state = self.states[-1]
        self.transition_matrix[current_state][next_state] = p
        self.duration_matrix[current_state][next_state] = t
        return self

    def to_matrix(self, from_list: dict) -> List[List[float]]:
        """
        Convert the transition matrix to a 2D list of floats.

        :returns:
            List[List[float]]: The transition matrix as a 2D list of floats.
        """
        n: int = len(self.states)
        matrix: List[List[float]] = [[0 for _ in range(n)] for _ in range(n)]
        for i, state in enumerate(self.states):
            for j, next_state in enumerate(self.states):
                matrix[i][j] = from_list[state].get(next_state, 0)
        return matrix

    def to_duration_matrix(self) -> List[List[float]]:
        return self.to_matrix(self.duration_matrix)

    def to_transition_matrix(self) -> List[List[float]]:
        return self.to_matrix(self.transition_matrix)

    def print_matrix(self):
        """
        Print the transition matrix in a human-readable format.
        """
        matrix = self.to_transition_matrix()
        n = len(self.states)
        # find the max length of state names
        max_state_len = len(max(self.states, key=len))
        print(" " * (max_state_len + 1), *self.states)
        for i, state in enumerate(self.states):
            # padding spaces to align the columns
            if round(sum(matrix[i]), 2) == 1.0:
                print(f"{state:<{max_state_len}}  ", end="")
                for j in range(n):
                    print(f"{matrix[i][j]:<{max_state_len}} ", end="")
            else:
                print_color(f"{state:<{max_state_len}}  ", color=BgColors.FAIL, end="")
                for j in range(n):
                    print_color(f"{matrix[i][j]:<{max_state_len}} ", color=BgColors.FAIL, end="")
            print()
