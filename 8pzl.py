from pzl_types import Node, Problem


def main():
    pzl_selection = int(
        input(
            'Welcome to 862229357 8 puzzle solver.\nType "1" to use a default puzzle, or "2" to enter your own puzzle.'
        )
    )
    pzl = [[1, 2, 3], [4, 8, 0], [7, 6, 5]]  # default puzzle

    if pzl_selection == 2:
        print("Enter your puzzle, use a zero to represent the blank\n")

        # 1st row
        r1 = input("Enter the first row, use space or tabs between numbers:\n")
        r1 = list(map(int, r1.split()))
        # 2nd row
        r2 = input("Enter the second row, use space or tabs between numbers:\n")
        r2 = list(map(int, r2.split()))
        # 3rd row
        r3 = input("Enter the third row, use space or tabs between numbers:\n")
        r3 = list(map(int, r3.split()))

        # combines input into a single puzzle
        pzl = [r1, r2, r3]

    # Ensure puzzle is valid
    if len(pzl) != 9 or set(pzl) != set(range(9)):
        print("Invalid puzzle configuration!")
        return

    algo_choice = int(
        input(
            "\nEnter your choice of Algorithm: \n1) Uniform Cost Search"
            "\n2) A* with the Misplaced Tile Heuristic \n3) A* with the Manhattan Distance Heuristic\n"
        )
    )

    problem = Problem(pzl)


if __name__ == "__main__":
    main()
