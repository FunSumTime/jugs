class Node:
    def __init__(self, state, parent=None, action=None, cost=0, cap):
        self.state = state  # The current state of the jugs (e.g., a tuple: (2, 0))
        self.parent = parent  # Reference to the node that created this one
        self.cost = cost  # The number of steps to reach this state
        self.capacity = cap

