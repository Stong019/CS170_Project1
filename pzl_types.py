import queue
class Node:
    def __init__(self, state, parent=None, action=None, gn=0):
        self.state = state
        self.parent = parent
        self.action = action  # needed for reconstructing the path
        self.gn = gn  # cost from start node to current node
        self.hn = 0  # est heuristic cost from current node to the goal node
        self.fn = 0  # gn + hn

    def __lt__(self, other):
        return self.fn < other.fn
    
    def get_state(self):
        return self.state

    def set_gn(self, gn):
        self.gn = gn
    
    def get_gn(self):
        return self.gn

    def set_hn(self, hn):
        self.hn = hn

    def get_hn(self):
        return self.hn
    
    def set_fn(self, fn):
        self.fn = fn

    def get_fn(self):
        return self.fn


class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.visited_states = set()

    def goal_test(self, state):
        return self.goal_state == state

    def is_visited(self, state):
        if tuple(state) in self.visited_states:
            return True
        # return false so we know to visit the children of the states
        self.visited_states.add(tuple(state))
        return False

    def get_b_pos(self, state) :
        for i, row in enumerate(state):
            if 0 in row:
                return (i, row.index(0))  # returns a tuple of (row, col)
            
    def misplaced_tile(self, state):
        m_cnt = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if int(state[i][j]) != self.goal_state[i][j] and int(state[i][j]) != 0:
                    m_cnt += 1
        return m_cnt
    
    def euclidean_dist(self, state):
        dist = 0
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] != 0:
                    gr = (state[r][c] - 1) // 3  
                    gc = (state[r][c] - 1) % 3
                    dist += ((gr - r) ** 2 + (gc - c) ** 2) ** 0.5
        return dist


    def operators(self, input_node, algo_choice) :
        curr_state = input_node.state
        row, col = self.get_b_pos(curr_state)
        directions = [(-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")]
        operator_list = []

        for dr, dc, action in directions:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < 3 and 0 <= new_col < 3
            ):  # check if the new node is in bounds
                new_state = [r[:] for r in curr_state]  # deep copy of 2D list
                new_state[row][col], new_state[new_row][new_col] = (
                    new_state[new_row][new_col],
                    new_state[row][col],
                )
                if not self.is_visited(new_state):
                    new_node = Node(
                        new_state,
                        parent=input_node,
                        action=action,
                        gn=input_node.gn + 1,
                    )
                    if algo_choice == 1:
                        new_node.hn = 0
                    if algo_choice == 2:
                        new_node.hn = self.misplaced_tile(self.initial_state)
                    if algo_choice == 3:
                        new_node.hn = self.euclidean_dist(self.initial_state)

                    operator_list.append(new_node)
        return operator_list
    
    def state(self):
        return self.initial_state
    
def search(problem, algo_choice):
    nodeQueue = queue.PriorityQueue()
    startNode = Node(problem.state())
    startNode.set_gn(0)
    startNode.set_hn(0)
    startNode.set_fn(0)
    nodeQueue.put(startNode)
    print("Expanding state")
    while(1):
        if nodeQueue.empty():
            return "failure"
        node = nodeQueue.get()
        if problem.goal_test(node.get_state()):
            print("Goal!!")
            print("To solve this problem the search algorithm expanded a total of {node_total} nodes".format(node_total = problem.get_node_count()))
            print("The maximum number of nodes in the queue at any one time was {max_queue_nodes}.".format(max_queue_nodes=maxQueueSize))
            print("The depth of the goal node was {depth}".format(depth=node.get_gn()))
            return node
        print("The best state to expand with a g(n) = {gn} and h(n) = {hn} is ...".format(gn=node.get_gn(), hn=node.get_hn()))
        ##tile_print(node)
        for index, tile in enumerate(node.get_state()):
            if tile == 0:
                print("b", end=' ')
            else:
                print(tile, end=' ')
            if index % 3 == 2:
                print()
        print()
        newNodes = problem.operator(node, algo_choice)
        for node in newNodes:
            nodeQueue.put(node)
