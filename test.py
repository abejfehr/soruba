def test(function, value, expected):
  print "value: " + str(value)
  print "expected return: " + str(expected)
  print "actual return:   " + str(function(value))
  if expected == function(value):
    print "PASS"
  else: print "FAIL"

from sudokusolver import *

p = ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"

#q = generate_candidate_puzzle(p)

#print q[0]
#print 25*" "
#print q[1]
#print 25*" "
#print q[2]

solve_sudoku(p)

"""
print textify(q)

print "Testing get_coords"
print "=================="
test(get_coords, 0, ([0,0],[0,0],[0,0]))
test(get_coords, 3, ([0,3],[3,0],[1,0]))
test(get_coords, 9, ([1,0],[0,1],[0,3]))
test(get_coords, 43, ([4,7],[7,4],[5,4]))
test(get_coords, 80, ([8,8],[8,8],[8,8]))


print "Testing get_knowns"
print "=================="
test(get_knowns, q[0][0], None)
"""

#f = open("msk_009.txt", "r")
#for line in f.readlines():
#  print solve_sudoku(line.strip())
#f.close()
