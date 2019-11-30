import sys
import time

from DiscreteSolver import DiscreteSolver

chess_board_size = int(sys.argv[1])

N = list(range(chess_board_size))

domain = {i: N for i in N}

solver = DiscreteSolver(domain)


# add constraints
def make_constraint(line1, line2):
    return lambda col1, col2: col1 - col2 not in {line1 - line2, 0, line2 - line1}


for line2 in N:
    for line1 in range(line2):
        solver.add_constraint(line1, line2, make_constraint(line1, line2))

start_time = time.time()
solution = solver.solve(compatibility_check='forward')
duration = time.time() - start_time

# display solution
for i in N:
    for j in N:
        if solution[i] == j:
            print("* ", end='')
        else:
            print(". ", end='')
    print()


"""
On my computer:
Using forward compatibility check:
    Chess board size: 100, execution time: 0.16s
    Chess board size: 200, execution time: 2.87s
    Chess board size: 300, execution time: 4.16s
    Chess board size: 400, execution time: 11.26s
    Chess board size: 500, execution time: 20.24s
    Chess board size: 600, execution time: 111.64s
Using backward compatibility check:
    Chess board size: 10, execution time: 0.01s
    Chess board size: 15, execution time: 0.10s
    Chess board size: 18, execution time: 3.98s
    Chess board size: 25, execution time: 8.04s
"""

print("Time to solve: ", duration)
