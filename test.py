from sudokusolver import *

f = open("msk_009.txt", "r")
for line in f.readlines():
  print solve_sudoku(line.strip())
f.close()
