def main():
    print('Welcome to 862229357 8 puzzle solver.')

    puzzle_input = input('Type "1" to use a default puzzle, or "2" to enter your own puzzle.')
    num = int(puzzle_input)
    #print(num)

    if num == 1:
        puzzle = (['1','2','3'],['4','8','0'],['7','6','5'])
    
    elif num == 2:
        print("Enter your puzzle, use a zero to represent the blank\n")

        # 1st row
        r1 = input('Enter the first row, use a zero to represent the blank:\n')
        r1 = r1.split(' ')
        # 2nd row
        r2 = input('Enter the second row, use space or tabs between numbers:\n')
        r2 = r2.split(' ')
        # 3rd row
        r3 = input('Enter the thrid row, use space or tabs between numbers: \n')
        r3 = r3.split(' ')

        print('\n')#just for spacing

        # Pzl :: Puzzle, combines input into a single puzzle
        Pzl = r1, r2, r3
        
        algo_choice = input('Enter your choice of Algorithm: \n1) Uniform Cost Search' 
                            '\n2) A* with the Misplaced Tile Heuristic \n3) A* with the Euclidean Distance Heuristic')
    
        algo_choice = int(algo_choice)
        
        print(search(Pzl, algo_choice))


def search(Puzzle, Algorithm):
    return 0

if __name__ == "__main__":
    main()