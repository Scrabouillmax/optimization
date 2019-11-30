import sys

from DiscreteSolver import DiscreteSolver

chess_board_size = int(sys.argv[1])

N = list(range(chess_board_size))

domain = {i: N for i in N}

solver = DiscreteSolver(domain)


def make_constraint(line1, line2):
    return lambda col1, col2: col1 - col2 not in {line1 - line2, 0, line2 - line1}


# add constraints
for line2 in N:
    for line1 in range(line2):
        solver.add_constraint(line1, line2, make_constraint(line1, line2))

solution = solver.solve()

# display solution
for i in N:
    for j in N:
        if solution[i] == j:
            print("* ", end='')
        else:
            print(". ", end='')
    print()
