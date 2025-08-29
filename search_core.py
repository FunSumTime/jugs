 from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, cap):
        self.state = state  # The current state of the jugs (e.g., a tuple: (2, 0))
        self.parent = parent  # Reference to the node that created this one
        self.cost = cost  # The number of steps to reach this state
        self.capacity = cap

# gloabal varables 
capacities = [8,5,3]
start = [8,0,0]
initail_node = Node(state=start)
goalstate = [4,4,0]

def Actions(state):
    actions = []
    num_jugs = len(state)
    
    # Pour from jug i to jug j
    for i in range(num_jugs):
        for j in range(num_jugs):
            if i != j:
                actions.append((i, j))
    return actions

def transitive(state, action):
   # Make a copy of the original state list to avoid modification
    new_state = list(state)
    
    source_jug_index, dest_jug_index = action[0], action[1]
    
    source_current_level = new_state[source_jug_index]
    dest_capacity = capacities[dest_jug_index]
    dest_current_level = new_state[dest_jug_index]
    
    amount_empty = dest_capacity - dest_current_level
    amount_to_pour = min(source_current_level, amount_empty)
    
    new_state[source_jug_index] -= amount_to_pour
    new_state[dest_jug_index] += amount_to_pour
    
    return new_state # Returns a list




def isgoal(state,goal):
    return state == goal

# recurse up the parent path
def getpath(node):
    path = []
    path.append([node.state,node.action])
    parent = node.parent
    while parent:
        
        path.append([parent.state, parent.action])
        parent = parent.parent
    # could also do this with slicing ex [::-1] would reverse it
    return path[::-1]


def bfsSearch(initail_node):
    frontier = deque
    frontier.append(initail_node)
    visted = {initail_node.state}
    while frontier:
        n = frontier.popleft()
        if(isgoal(n.state,goalstate)):
            # we found the goal
            return getpath(n)
        for i in Actions(n.state):

            s = transitive(n.state,i)
            new_state = Node(state=s, parent=n, action=i,cap=n.cost+1)
            if(new_state.state not in visted):
                visted.append(new_state.state)
                frontier.append(new_state)
    

    # return failur
    return []



