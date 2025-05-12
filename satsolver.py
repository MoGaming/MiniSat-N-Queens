import subprocess

# n queens problem in MiniSat
n = 4
totalPositions = n**2
clauses = []

def getDiagonal(index): 
    positions = []
    row = (index - 1) // n
    col = (index - 1) % n
    
    r = row + 1
    c = col + 1
    while r < n and c < n:
        positions.append(r * n + c + 1)
        r += 1
        c += 1
    
    r = row + 1
    c = col - 1
    while r < n and c >= 0:
        positions.append(r * n + c + 1)
        r += 1
        c -= 1
    
    return positions

for index in range(n): # queen positions
    row_clause = []
    for j in range(n):
        row_clause.append(str(index * n + j + 1))
    clauses.append(" ".join(row_clause)) # atleast one queen in row
    col_clause = []
    for j in range(n):
        col_clause.append(str(index + 1 + n*j))
    clauses.append(" ".join(col_clause)) # atleast one queen in col
    col = index + 1
    for i in range(n): # queen attacks, atleast most one queen in each row and col
        for position in getDiagonal(index + 1 + i*n): # all bottom left and bottom right queen attacks
            clauses.append("-" + str(index + 1 + i*n) + " -" + str(position))
        for j in range(col, n): # row queen attacks
            clauses.append("-" + str(col + n * i) + " -" + str(j + 1 + n * i)) 
        for j in range(i+1, n): # col queen attacks
            clauses.append("-" + str(col + n * i) + " -" + str(col + n * j))

clauses.sort() # to make it easier to read 

# define a simple CNF formula and write to a file 
cnf_data = "p cnf " + str(totalPositions) + " " + str(len(clauses)) + "\n"
for clause in clauses:
    cnf_data = cnf_data + clause + " 0\n"

with open("input.cnf", "w") as f:
    f.write(cnf_data)

# run MiniSat
result = subprocess.run(
    ["minisat", "input.cnf", "output.txt"],
    capture_output=True, text=True
)

# run output results
with open("input.cnf") as f:
    print("Contents of input.cnf:\n", f.read().strip())
with open("output.txt") as f:
    print("\nContents of output.txt:")
    string = f.read().strip().split()
    print(string[0])
    if string[0] != "UNSAT":
        string = string[1:n**2+1]
        for i in range(n):
            line = ""
            for j in range(n): # format each boolean character, n=31 is last size that this can display variables nicely
                number = string[j + n*i]
                if 4 - len(number) == 2:
                    number = "  " + number
                elif 4 - len(number) == 3:
                    number = "   " + number
                elif 4 - len(number) == 1:
                    number = " " + number
                line = line + number + " "
            print(line)

print("\nMiniSat return code:\n", result.returncode)  # 10 means SAT, 20 means UNSAT
print("\nMiniSat console output:\n", result.stdout.strip())
