"""
A Sukoku solver from a binary linear programming point of view.
It solves a random sudoku from 'https://www.sudoku-online.org/extremo.php'

Author: Carlos Sebastián Martínez-Cava
"""

import pulp
from selenium import webdriver
from time import sleep

values = rows = cols = range(1, 10)

problem = pulp.LpProblem("Sudoku Problem", pulp.LpMinimize)  # We have created the problem
problem += 0, "An arbitrary objective function"  # No solution is better than other

choices = pulp.LpVariable.dicts("Choice", (values, rows, cols), cat='Binary')  # Create the decision variable

# Now we introduce the restrictions associated with a standard sudoku

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

# We get into the page in which we are going to solve the random sudoku we obtain in there
browser = webdriver.Chrome()
browser.get('https://www.sudoku-online.org/extremo.php')

sleep(1)  # Just to let the page load

cont = 0
input_data = []

# We go through the sudoku element by element

for r in rows:
    for c in cols:
        element = browser.find_element_by_id('sudo_input_' + str(cont))
        try:  # If we find a number in a cell, then we store the information to introduce later a restriction
            value = float(element.text)
            input_data.append((value, r, c))
            cont = cont + 1
        except:  # If not, we simply continue
            cont = cont + 1

for (v, r, c) in input_data:  # As we said, we introduce the restrictions associated with the information we got
    problem += choices[v][r][c] == 1

problem.writeLP('Sudoku.lp')

problem.solve()  # Finally, we solve the sudoku as a binary linear programming problem
print("Status: ", pulp.LpStatus[problem.status])

out_file = open('sudokuout.txt', 'w')

numpad = ['\ue01b', '\ue01c', '\ue01d', '\ue01e', '\ue01f', '\ue020', '\ue021', '\ue022', '\ue023']
cont = 0

# To finish, we write the solved sudoku in the page and in a .txt  file

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
                if (v, r, c) in input_data:
                    cont = cont + 1
                else:
                    element = browser.find_element_by_id('sudo_input_' + str(cont))
                    element.click()
                    element.send_keys(numpad[v - 1])
                    cont = cont + 1
    if r == 9:
        out_file.write("+---------+---------+---------+")

out_file.close()

print('The solution is also in "sudokuout.txt" file')
