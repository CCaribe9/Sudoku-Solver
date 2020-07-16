"""
A Sukoku solver from a binary linear programming point of view.

Author: Carlos Sebastián Martínez-Cava
"""

import pulp

sequence = range(1, 10)
values = sequence
rows = sequence
cols = sequence

problem = pulp.LpProblem("Sudoku Problem", pulp.LpMinimize)  # We have created the problem
problem += 0, "An arbitrary objective function"  # No solution is better than other

choices = pulp.LpVariable.dicts("Choice", (values, rows, cols), cat='Binary')  # Create the decision variable

for r in rows:
    for c in cols:
        problem += pulp.lpSum([choices[v][r][c] for v in values]) == 1
for v in values:
    for c in cols:
        problem += pulp.lpSum([choices[v][r][c] for r in rows]) == 1
    for r in rows:
        problem += pulp.lpSum([choices[v][r][c] for c in cols]) == 1
    for p in range(1, 8, 3):
        for q in range(1, 8, 3):
            problem += pulp.lpSum([choices[v][p + i][q + j] for i in range(0, 3) for j in range(0, 3)]) == 1

# The starting numbers are entered as constraints
in_file = open('sudokuin.txt', 'r')

aux = in_file.readlines()
input_data = []
cont = -1
for i in aux:
    cont = cont + 1
    i = i.split()
    if i == ['+---------+---------+---------+']:
        aux.pop(cont)
for i in range(len(aux)):
    aux2 = aux[i].split()
    for j in range(1, len(aux2) - 1):
        if j != 4 and j != 8 and aux2[j] != '0':
            if 4 < j < 8:
                input_data.append((int(aux2[j]), i+1, j - 1))
            elif j > 8:
                input_data.append((int(aux2[j]), i+1, j - 2))
            elif j < 4:
                input_data.append((int(aux2[j]), i+1, j))

in_file.close()

for (v, r, c) in input_data:
    problem += choices[v][r][c] == 1


problem.writeLP('Sudoku.lp')

problem.solve()
print("Status: ", pulp.LpStatus[problem.status])


out_file = open('sudokuout.txt', 'w')

for r in rows:
    if r == 1 or r == 4 or r == 7:
        out_file.write("+---------+---------+---------+\n")
    for c in cols:
        for v in values:
            if choices[v][r][c].varValue == 1:
                if c == 1 or c == 4 or c == 7:
                    out_file.write('|')
                out_file.write(' ' + str(v) + ' ')
                if c == 9:
                    out_file.write('|\n')
    if r == 9:
        out_file.write("+---------+---------+---------+")

out_file.close()
