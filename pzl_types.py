class Node:
    def __init__(self, state, parent=None, action=None, gn=0):
        self.state = state
        self.parent = parent
        self.action = action  # needed for reconstructing the path
        self.gn = 0  # cost from start node to current node
        self.hn = 0  # est heuristic cost from current node to the goal node
        self.fn = 0  # gn + hn

    def __lt__(self, other):
        return self.fn < other.fn


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

    def get_b_pos(self, state) -> tuple(int, int):
        for i, row in enumerate(state):
            if 0 in row:
                return (i, row.index(0))  # returns a tuple of (row, col)

    def operators(self, input_node) -> list(Node):
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
                    operator_list.append(new_node)
        return operator_list
