"""
see: https://puzzling.stackexchange.com/questions/93030/prime-number-snake
"""
import time

def primes_less_or_equal(n):
    l = [True] * (n + 1)
    for factor in range(2, n // 2):
        for i in range(2 * factor, n+1, factor):
            l[i] = False
    retval = []
    for i in range(2,n+1):
        if l[i]: 
            retval.append(i)
    return retval

# constants
N  = 10
N2 = N * N
PRIMES_BELOW_N2 = primes_less_or_equal(N2)
PRIME_POSITIONS = [ # values from problem definition 
                    (0,2), 
                    (1,1), (1,7), (1,9), 
                    (2,2), (2,4), (2,6), 
                    (3,1), (3,5),
                    (4,4), (4,6), 
                    (5,1), (5,4), (5,5), (5,9), 
                    (6,2), (6,4), (6,8),
                    (7,1), (7,3), (7,7),
                    (8,0), (8,4),
                    (9,3), (9,5)
                  ]
SHOW_PROGRESS_TRIES = 5000

# globals
board = None
tries = 0
best_so_far = 0
str_solutions = set()

def on_board(i,j):
    return i >= 0 and i < N and j >= 0 and j < N

def all_neighbours(i,j):
    return [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]

def valid_neighbours(i,j):
    return [neigh for neigh in all_neighbours(i,j) if on_board(*neigh)]

def create_board():
    board = {}
    for i in range(10):
        for j in range(10):
            board[(i,j)] = {
                'occupies'        : 0,  # 0 means not occupied (yet)
                'should_be_prime' : (i,j) in PRIME_POSITIONS,
                'neighbours'      : valid_neighbours(i,j)
            }
    return board

def stringify_board():
    global board

    result = "\n +----------------------------------------------------+\n"    
    for i in range(N):
        result += " | "
        for j in range(N):
            prime = "*" if board[(i,j)]["should_be_prime"] else " "
            number = board[(i,j)]["occupies"]
            number = f"{number:3}" if number else "   "
            result += f"{number}{prime} "
        result += " | \n"
    result += " +----------------------------------------------------+\n\n"
    
    return result

def print_board():
    print(stringify_board())


def free_space_at(free,i,j):
    if not (i,j) in free:
        return 0
    else:
        free.remove((i,j))
        return ( 1 + free_space_at(free, i-1,j  )
                   + free_space_at(free, i+1,j  )
                   + free_space_at(free, i  ,j-1)
                   + free_space_at(free, i  ,j+1) )

def enough_space_for_the_tail(number, i, j):
    global board
    free = [key for key, item in board.items() if not item['occupies']]
    n = free_space_at(free,i,j)
    return (101 - number) <= n


def try_it(number, i, j):
    global board, tries, best_so_far, str_solutions
    tries += 1
    
    # print some progres
    best_so_far = max(best_so_far, number)
    if (tries % SHOW_PROGRESS_TRIES) == 0:
        print(tries, number, best_so_far, end="\r")

    # check for succes, if number equals 101, the previous 100 are oke!    
    if number == 101:
        # Hurray, we are finished, return succes
        print("Hurray")
        print(tries, number)
        print_board()
        str_solutions.add(stringify_board())
        return False # return True to stop at the first found solutioon
    
    # check if this is a valid move
    if board[(i,j)]["occupies"]:
        return False
    
    if (number in PRIMES_BELOW_N2) != board[(i,j)]["should_be_prime"]:
        return False
    
    if not enough_space_for_the_tail(number, i, j):
        return False
        
    # let's make our move, ...
    board[(i,j)]["occupies"] = number
    
    # ..., and try the next steps, ...
    for neigh in board[(i,j)]["neighbours"]:
        next_i, next_j = neigh
        if try_it(number + 1, next_i, next_j):
            # Hurray, succes
            return True
    
    # Nope, this move did not work, undo and return failure
    board[(i,j)]["occupies"] = 0    
    return False


def main():
    global board, tries, str_solutions
    
    start_time = int(time.time())
    
    board = create_board()
    for i in range(N):
        for j in range(N):
            try_it(1, i, j)

    end_time = int(time.time())
            
    print("\n\n=========================================\n\n")
    for sol in str_solutions:
        print(sol)
    print("Number of solutions       : ", len(str_solutions))
    print("Number of tries           : ", tries)
    print("Computation time (seconds): ", str(end_time - start_time))

if __name__ == "__main__":
    main()

