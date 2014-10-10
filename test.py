from sudokusolver import *

p = ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"

print get_candidate_rows(p)
print " "*25
print get_candidate_cols(p)
print " "*25
print get_candidate_boxes(p)

#f = open("msk_009.txt", "r")
#for line in f.readlines():
#  print solve_sudoku(line.strip())
#f.close()
