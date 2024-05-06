import queue


class Node:
    def __init__(self, state, parent=None, action=None, gn=0, hn=0):
        self.state = state
        self.parent = parent
        self.action = action  # needed for reconstructing the path
        self.gn = gn  # cost from start node to current node
        self.hn = hn  # est heuristic cost from current node to the goal node
        self.fn = self.gn + self.hn  # gn + hn

    def __lt__(self, other):
        return self.fn < other.fn

    def get_state(self):
        return self.state

    def update_costs(self, gn, hn):
        self.gn = gn
        self.hn = hn
        self.fn = self.gn + self.hn


class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.visited_states = {}
        self.expanded_cnt = 0
        self.max_node_cnt = 0

    def goal_test(self, state):
        return self.goal_state == state

    def get_b_pos(self, state):
        for i, row in enumerate(state):
            if 0 in row:
                return (i, row.index(0))  # returns a tuple of (row, col)

    def misplaced_tile(self, state):
        m_cnt = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != 0 and state[i][j] != self.goal_state[i][j]:
                    m_cnt += 1
        return m_cnt

    def manhattan_dist(self, state):
        dist = 0
        for r in range(len(state)):
            for c in range(len(state[r])):
                val = state[r][c]
                if val != 0:
                    target_r = (val - 1) // 3
                    target_c = (val - 1) % 3
                    dist += abs(target_r - r) + abs(target_c - c)
        return dist

    def operators(self, input_node, algo_choice):
        curr_state = input_node.get_state()
        row, col = self.get_b_pos(curr_state)
        directions = [(-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")]
        operator_list = []
        self.expanded_cnt += 1

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
                state_tuple = tuple(tuple(x) for x in new_state)
                if state_tuple not in self.visited_states:
                    gn = input_node.gn + 1
                    hn = 0
                    if algo_choice == 2:
                        hn = self.misplaced_tile(new_state)
                    elif algo_choice == 3:
                        hn = self.manhattan_dist(new_state)
                    new_node = Node(
                        new_state, parent=input_node, action=action, gn=gn, hn=hn
                    )
                    operator_list.append(new_node)
                    self.visited_states[state_tuple] = new_node
                elif input_node.gn + 1 < self.visited_states[state_tuple].gn:
                    # Update node in priority queue
                    self.visited_states[state_tuple].update_costs(
                        input_node.gn + 1, self.visited_states[state_tuple].hn
                    )
                    operator_list.append(self.visited_states[state_tuple])
        return operator_list


def search(problem, algo_choice):
    nodeQueue = queue.PriorityQueue()
    initial_hn = 0
    if algo_choice == 2:
        initial_hn = problem.misplaced_tile(problem.initial_state)
    elif algo_choice == 3:
        initial_hn = problem.manhattan_dist(problem.initial_state)
    startNode = Node(problem.initial_state, gn=0, hn=initial_hn)
    nodeQueue.put(startNode)
    problem.visited_states[tuple(tuple(x) for x in problem.initial_state)] = startNode

    while not nodeQueue.empty():
        node = nodeQueue.get()
        if problem.goal_test(node.get_state()):
            print("Goal!!")
            print(
                f"To solve this problem the search algorithm expanded a total of {problem.expanded_cnt} nodes"
            )
            print(
                f"The maximum number of nodes in the queue at any one time was {problem.max_node_cnt}."
            )
            print(f"The depth of the goal node was {node.gn}")
            return node
        print(
            f"The best state to expand with a g(n) = {node.gn} and h(n) = {node.hn} is:"
        )
        for row in node.get_state():
            print(" ".join(str(x) if x != 0 else "b" for x in row))
        print()
        newNodes = problem.operators(node, algo_choice)
        for newNode in newNodes:
            nodeQueue.put(newNode)
            if nodeQueue.qsize() > problem.max_node_cnt:
                problem.max_node_cnt = nodeQueue.qsize()
