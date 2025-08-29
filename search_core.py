from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, cap=None, depth=0):
        self.state = state  # The current state of the jugs (e.g., a tuple: (2, 0))
        self.action = action # action made to get here
        self.parent = parent  # Reference to the node that created this one
        self.cost = cost  # The number of steps to reach this state
        self.capacity = cap
        self.depth = depth

IDFSGenerated = 1
BFSGenerated = 1
Max_frontier_size = 0
BFSDethp = 0
IDDepth = 0
IDCost = 0
BFSCost = 0

initail_node = Node(state= [8,0,0], cap=[8,5,3])
goalstate = [4,4,0]

def Actions(state):
    actions = []
    num_jugs = len(state)
    
    # Pour from jug i to jug j
    # get all the permutaions
    #  or ways i can order two from three
    for i in range(num_jugs):
        for j in range(num_jugs):
            if i != j:
                actions.append((i, j))
    return actions

def transitive(state, action,capacities):
   # Make a copy of the original state list to avoid modification
    new_state = list(state)
    # left side is the jug moving

    source_jug_index, dest_jug_index = action[0], action[1]
    # check how much is in the jug
    source_current_level = new_state[source_jug_index]
    # how much the reciving jug can hold cap
    dest_capacity = capacities[dest_jug_index]
    # its actual level in the enviroment
    dest_current_level = new_state[dest_jug_index]
    # how much it can hold right now aka space
    amount_empty = dest_capacity - dest_current_level
    # this is saying either fill it up all the way or take all thats from the source and fill it in the destination
    amount_to_pour = min(source_current_level, amount_empty)
    
    new_state[source_jug_index] -= amount_to_pour
    new_state[dest_jug_index] += amount_to_pour
    
    return new_state # Returns a list




def isgoal(state,goal):
    return state == goal

# recurse up the parent path
def getpath(node):
    path = []
    # Loop from the goal node back to the start
    while node:
        path.append((node.state, node.action))
        node = node.parent
    
    # Reverse the path to get it in the correct order (start to goal)
    path = path[::-1]
    
    # Clean up the initial node entry
    if path and path[0][1] is None:
        path[0] = (path[0][0], "Start")
    return path


def bfsSearch(initail_node):
    # class constructor not a varable
    global BFSCost, BFSDethp, BFSGenerated, Max_frontier_size
    frontier = deque()
    frontier.append(initail_node)
    visited = [initail_node.state]
    while frontier:
        n = frontier.popleft()
        if(isgoal(n.state,goalstate)):
            # we found the goal
            BFSDethp = n.cost
            BFSCost = n.cost
            return getpath(n)
        for i in Actions(n.state):

            s = transitive(n.state,i,n.capacity)
            if(s not in visited):
                new_state = Node(state=s, parent=n, action=i,cost=n.cost+1,cap=n.capacity)
                visited.append(new_state.state)
                BFSGenerated +=1
                frontier.append(new_state)
                if(Max_frontier_size < len(frontier)):
                    Max_frontier_size = len(frontier)
    

    # return failur
    return None

def IDFS(initail_node, Limit):
    global IDCost, IDDepth, IDFSGenerated
    stack = []
    stack.append(initail_node)
    visited = [initail_node.state]
    cuttoff = False
    while stack:
        n =  stack.pop()
        if(isgoal(n.state,goalstate)):
            IDCost = n.cost
            IDDepth = n.depth
            return getpath(n)
        if n.depth >= Limit:
            cuttoff = True
            continue
        A = Actions(n.state)[::-1]
        for i in A:
            s = transitive(n.state,i,n.capacity)
            if s not in visited:
                new_node = Node(state=s, parent=n, action=i, cost=n.cost + 1, cap=n.capacity, depth=n.depth + 1)
                visited.append(s)
                stack.append(new_node)
                IDFSGenerated += 1

    
    if(cuttoff):
        # function needs to be called again with new cuttoff
        return 'cutoff'
    else:
        return None

def IDFS_Caller(initial_node, max_depth=50):
    for limit in range(max_depth):
        # Call the IDFS helper with an increasing depth limit
        result = IDFS(initial_node, limit)

        # Check the result of the IDFS call
        if result == "cutoff":
            # Goal not found but the search was cut off. Continue to the next depth.
            continue
        elif result is not None:
            # A solution was found! Return it and stop the search.
            return result
        else:
            # The search space was exhausted without a solution. The goal is unreachable.
            return None
    
    return None



#  case one
# a = bfsSearch(initail_node)
# b = IDFS_Caller(initail_node)
c = bfsSearch(initail_node_2)
d = IDFS_Caller(initail_node_2)
print(a)
print(b)
print("BFS statistics: Generated " + str(BFSGenerated) + " Depth: " + str(BFSDethp) + " Cost: "  + str(BFSCost) + " Max Size: " +str(Max_frontier_size)  )
print("IDFS statistics: Generated " + str(IDFSGenerated) + " Depth: " + str(IDDepth) + " Cost: "  +  str(IDCost)  )
# generated and expanded would be the same as we get rid of duplicates

