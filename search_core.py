# this is a program that runs on the Game jugs
# goal of the game is to get the water in the jugs to a specifc value
#  you can pour one into another but cant overfill them
# this Will use a search algroithm to find the path for the goal result
# there is metrics and all that will show what happend and so on
# The algortitims used are BFS (Breath first search) and IDFS (Iterative Depth First Search)
#  they use the graph varerent where they use a list to keep track of the ones they visted
# this was a good project and fun for AI and to figure out how Actions and Transitvie fucntions work
# and how to work towards a goal. Aug 29 2025


from collections import deque
# defintion of Node we will use to pass around
class Node:
    def __init__(self, state, parent=None, action=None, cost=0, cap=None, depth=0):
        self.state = state  # The current state of the jugs (e.g., a tuple: (2, 0))
        self.action = action # action made to get here
        self.parent = parent  # Reference to the node that created this one
        self.cost = cost  # The number of steps to reach this state
        self.capacity = cap
        self.depth = depth
# global varables
IDFSGenerated = 1
BFSGenerated = 1
Max_frontier_size = 0
BFSDethp = 0
IDDepth = 0
IDCost = 0
BFSCost = 0


# action function that will return the actions avalable on the state of the game
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

# transitive fucnton that will take a state and a action and produce a new state
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



#  returns if the goal state is reached, takes in a state and the goal state
def isgoal(state,goal):
    return state == goal

# recurse up the parent path
# makes a list and reverses it
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

# Natural BFS search with a vist list to make it not loop over ones it already checked
def bfsSearch(initail_node):
    # so we can acces these in the function
    global BFSCost, BFSDethp, BFSGenerated, Max_frontier_size
    # class constructor not a varable
    frontier = deque()
    frontier.append(initail_node)
    # add the first node to frontier and visted
    visited = [initail_node.state]
    while frontier:
        # take the frist node in the queue
        n = frontier.popleft()
        # check if we reached the end
        if(isgoal(n.state,goalstate)):
            # we found the goal
            BFSDethp = n.cost
            BFSCost = n.cost
            # return the path we took to get here
            return getpath(n)
        # loop over the actions we get back and aply all
        for i in Actions(n.state):
            # get the new state
            s = transitive(n.state,i,n.capacity)
            # if its not one we have seen add it
            if(s not in visited):
                # create new node with the parent being the old one and the state being the new state and update the cost
                new_state = Node(state=s, parent=n, action=i,cost=n.cost+1,cap=n.capacity)
                visited.append(new_state.state)
                BFSGenerated +=1
                frontier.append(new_state)
                if(Max_frontier_size < len(frontier)):
                    Max_frontier_size = len(frontier)
    

    # return failur
    return None
# does DFS but to a limit which is specified and will restart each time
def IDFS(initail_node, Limit):
    global IDCost, IDDepth, IDFSGenerated
    # DFS uses a stack so make one and add the first node and state to vistied
    stack = []
    stack.append(initail_node)
    visited = [initail_node.state]
    #  how we will keep track if we hit the limit
    cuttoff = False
    while stack:
        # take the first node of the stack
        n =  stack.pop()
        # check if we hit a goal
        if(isgoal(n.state,goalstate)):
            IDCost = n.cost
            IDDepth = n.depth
            return getpath(n)
        # check if we hit the limit if so recurse back up and go through other nodes
        # note: it doesent end the program it self just dosent go deeper
        if n.depth >= Limit:
            cuttoff = True
            continue
        # reverse the list we get back from actions so we can go down a branch all together as they will get put on the stack and not a queue
        A = Actions(n.state)[::-1]
        for i in A:
            # get the new state
            s = transitive(n.state,i,n.capacity)
            # check if we seen it yet
            if s not in visited:
                # if not make a new node and add it to the stack and update the depth + 1 
                new_node = Node(state=s, parent=n, action=i, cost=n.cost + 1, cap=n.capacity, depth=n.depth + 1)
                visited.append(s)
                stack.append(new_node)
                IDFSGenerated += 1

    
    if(cuttoff):
        # function needs to be called again with new cuttoff
        return 'cutoff'
    else:
        return None
# calls IDFS with a speicifed limit so it can recursivly go through the tree
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

# initail_node = Node(state= [8,0,0], cap=[8,5,3])
# goalstate = [4,4,0]

# a = bfsSearch(initail_node)
# b = IDFS_Caller(initail_node)
# print(a)
# print(b)


#  case two

initail_node_2 = Node(state = [1,3,5], cap=[3,5,8])
goalstate = [0,5,4]
c = bfsSearch(initail_node_2)
d = IDFS_Caller(initail_node_2)
print(c)
print(d)

# metrics printed
print("BFS statistics: Generated " + str(BFSGenerated) + " Depth: " + str(BFSDethp) + " Cost: "  + str(BFSCost) + " Max Size: " +str(Max_frontier_size)  )
print("IDFS statistics: Generated " + str(IDFSGenerated) + " Depth: " + str(IDDepth) + " Cost: "  +  str(IDCost)  )
# generated and expanded would be the same as we get rid of duplicates

