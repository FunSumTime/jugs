 from collections import deque
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


def getpath(state):


def bfsSearch(state):
    frontier = deque
    deque.append(state)
    while frontier:
        n = deque.popleft()
        if(isgoal(n,goalstate)):
            # we found the goal
            return getpath(n)
        for i in Actions(n):

            s = transitive(n,i)
            new_state = Node(state=s, parent=n, cap=n.cost+1)
            if(new_state.state not in visted):
                visted.append(new_state.state)
                deque.append(new_state)



