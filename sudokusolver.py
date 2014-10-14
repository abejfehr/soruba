###
# File:   sudokusolver.py
# Author: Abe Fehr
# Description: This file contains the functions required to solve any unsolved
#              sudoku puzzle. There is some important terminology which will be
#              passed around in the file, which goes as follows:
#
#  Sudoku Puzzle:    An 81 character long string with numbers for knowns and
#                    full stops(periods) for unknowns. Usually denoted by p
#  Cell:             Each of the 81 spaces that a number could occupy in the
#                    puzzle.
#  Row:              All of the cells which share the y coordinate in the puzzle
#  Column(col):      All of the cells which share the x coordinate in the puzzle
#  Box:							 All of the cells which belong to a 3x3 cell square, where
#                    the origin cell(top-left) has coordinates that are a
#                    multiple of 3.
#  Candidate Puzzle: The 81 element array which contains arrays with all the
#                    candidates that *could* possibly occupy each cell. Usually
#                    denoted by q
#	 Solved:           The state when each cell in a puzzle has only one candidate
#                    and the values are unique by row, box, and column
#  Valid:						 Not the same as a solved puzzle; when each cell has no
#                    less than one candidate. An invalid puzzle(one that
#                    contains zero candidates for a cell) is unsolvable.
###

Q = []
Q.append([])
for i in range(9):
	Q.append(range(i*9,i*9+9))
Q.append([])
for i in range(9):
	Q[1].append(i*9%9*9+i*9/9)
Q.append([[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],\
[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],\
[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]])


###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def solve_sudoku(p):
	q = generate_candidate_puzzle(p)
	return solve(q)

import copy

## from now on, q will be a candidate puzzle as such that it contains [[rows],
## [cols], [boxes]]

###
# Function: solve()
# Purpose:  recursively solves a sudoku puzzle
# Input:    puzzle - a canadate puzzle to solve
# Output:   the completed puzzle - an 81 character string of numbers
###
def solve(q):
	if not valid(q):
		return False

	if solved(q): return textify(q)

	#solve the trivial cases
	for i in range(9):
		for j in range(9):
			if len(q[0][i][j]) is 1:
				clear_candidates(i, q)

	h = 2
	while(not solved(q) and h < 4):
		#solve the squares with > 1 possibility
		for i in range(9):
			for j in range(9):
				if len(q[0][i][j]) is h:
					for k in range(h):
						nq = photocopy_puzzle_with(k, i*9+j, q)
						print textify(nq)
						print " " * (i*9+j) + "^"
#						print " " * (i*9+j-2) + str(q[0][i][j])
						print valid(nq)
						raw_input("Press Enter to Continue")
						result = solve(nq)
						if result:
							return result
#					print "none of them worked so I'm returning false"
					return False
		h += 1

	if solved(q): return textify(q)
	return False

def solve_old(q):
	if not valid(q):
		return False
	#go through every square in the puzzle
	for i in range(81):
		if len(q[i]) > 1:
			for j in range(len(q[i])):
				nq = photocopy_puzzle_with(j, i, q)
#				print textify(nq)
#				print " " * i + "^"
#				print " " * i + str(q[i])
#				print valid(nq)
#				raw_input("Press Enter to Continue")
				result = solve(nq)
				if result:
					return result
			return False
		else:
			clear_candidates(i, q)

	if solved(q): return textify(q)
	return False

###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def textify(q):
	s = []
	for i in range(9):
		for j in range(9):
			if len(q[0][i][j]) > 1: s.append(".")
			else: s.append(str(q[0][i][j][0]))
	return "".join(s)

###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def photocopy_puzzle_with(n, i, q):
	x = copy.deepcopy(q)
	c = get_coords(i)
	#convert the i to
	v = [x[0][c[0][0]][c[0][1]][n]]
	for y in range(3):
		x[y][c[y][0]][c[y][1]] = v
	clear_candidates(i, x)
	return x


def get_coords(i):
	return ([i/9,i%9],\
					[i%9,i/9],\
					[i/9/3*3+i%9/3,i/9%3*3+i%9%3])
"""
i is always the rolling coordinate
the inner coordinates are x and y where possible
i  x y
0  0 0  a = offset from the left edge of the puzzle = i % 9
1  0 1  x = offset from the left edge of the box = a % 3
2  0 2  b = offset from the top edge of the puzzle i / 9
3  1 0  y = offset from the top edge of the box = b % 3
4  1 1  k = 1 to 9 coordinate in the box = y * 3 + x
5  1 2  m = box coord from left = a / 3
6  2 0  n = box coord from top = b / 3
7  2 1  s = box relative to puzzle 1D coordinate b * 3 + a
"""

#the exact opposite of get_coords
def get_i(c):
	return c[0]*9+c[1]

###
# Function: generate_candidate_puzzle()
# Purpose:  generates a candidate puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def generate_candidate_puzzle(p):
	#the puzzle is already solved or isn't the correct length
	if not "." in p or len(p) is not 81: return False
	q = []
	q.append(get_candidate_rows(p))
	q.append(get_candidate_cols(p))
	q.append(get_candidate_boxes(p))
	return q

##
## The following functions are pretty damn crafty, I've gotta say. If you look
## closely, you'll notice that I'm using list comprehension, enumeration,
## ternary operators, slicing, and other advanced techniques. I'm able to
## accomplish an entire program in one line of code. Cool stuff
##

def get_candidate_rows(p):
	q = []
	for z in range(9):
		q.append([get_candidates(z*9+j,p) if x is "." else \
		[int(x)] for (j,x) in enumerate(p[z*9:z*9+9])])
	return q

def get_candidate_cols(p):
	q = []
	for z in range(9):
		q.append([get_candidates(j*9+z,p) if x is "." else \
		[int(x)] for (j,x) in enumerate(p[z::9])])
	return q

def get_candidate_boxes(p):
	q = []
	for m in [n for n in range(81) if n % 3 is 0 and (n / 9) % 3 is 0]:
		q.append([get_candidates(m+j%3+j/3*9,p) if x is "." else \
		[int(x)] for (j,x) in enumerate(p[m:m+3] + p[m+9:m+12] + p[m+18:m+21])])
	return q


###
# Function: get_candidates()
# Purpose:  gets the candidates for a particular position in the list
# Input:    i - the index of the node to calculate
# 	    		p - the puzzle to calculate it for
# Output:   list of the potential values for one node in the puzzle
###
def get_candidates(i, p):
	if p[i] is not ".":
		return [int(p[i])]
	#start with all of them
	c = range(1,10)
	row = get_row_known_set(i, p)
	col = get_col_known_set(i, p)
	box = get_box_known_set(i, p)
	c = [x for x in list(set(c) - set(row + col + box)) if x is not "."]
	if len(c) < 1: return False
	return c

###
# Function: get_row_set(i, p)
# Purpose:  solves a sudoku puzzle
# Input:    i - the index of the target cell
#           p - the sudoku puzzle
# Output:   the completed puzzle - an 81 character string of numbers
###
def get_row_known_set(i, p):
	return map(int, [x for x in p[i/9*9:i/9*9+9] if x is not "."])

###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def get_col_known_set(i, p):
	return map(int, [x for x in p[i%9::9] if x is not "."])

###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def get_box_known_set(i, p):
	m = 9 * (i / 9 / 3 * 3) + (i % 9 / 3 * 3)
	return map(int, [x for x in p[m:m+3] + p[m+9:m+12] + p[m+18:m+21] \
	if x is not "."])

###
# Function: clear_candidates()
# Purpose:  clears all the numbers from the related cells of the puzzle
# Input:    i - the index of the cell whose neighbours to clear
#						q - the full candidate puzzle to clear from
# Output:   boolean - whether or not any candidates were cleared from the
#           related squares
###
def clear_candidates(i, q):
	#TODO: fix this function. It *almost* works
	c = get_coords(i)

	#setup
	if len(q[0][c[0][0]][c[0][1]]) > 1: return
	flag = False

	for x in range(3): #go through the rows, cols and boxes
		for y in range(9): #go through the items in the each section
			ith_cell_of_current = q[x][c[x][0]][c[x][1]][0]
			neighbour_to_check = q[x][c[x][0]][y]
			if ith_cell_of_current in neighbour_to_check and c[x][1] is not y \
			and len(neighbour_to_check) > 1:
#				print c, y, x
#				print get_i([c[x][0],y])
#				if x is 0:
#					print "ASDF"
#					d = get_coords(get_i([c[x][0],y]))
#				if x is 1:
#					print "FDSA"
#					d = get_coords(get_i([y,c[x][0]]))
#				if x is 2:
#					print "ASSDF"
#					d = get_coords(c[x][1]+y/3 * 9 + c[x][0]+y%3)
				print "found candidate", ith_cell_of_current, "in q at position"
#				print q[0]
#				print 25*" "
#				print q[1]
#				print 25*" "
#				print q[2]
				q[x][c[x][0]][y].remove(ith_cell_of_current)
				flag = True
				if len(neighbour_to_check) is 1:
#					print "left it at one"
					clear_candidates(Q[x][c[x][0]][y], q)
	return flag

def get_i_special(x, i, y):
	if x is 0:
		i /= 9
		return i+y
	elif x is 1:
		i /= 9
		return (i+y) % 9 * 9 + (i+y) / 9
	elif x is 2:
		m = i % 9 / 3
		n = i / 9 / 3
		return n * 9 + m + (y % 3 * 9) + y / 3
	else: return False

###
# Function: valid()
# Purpose:  checks the validity of a candidate puzzle
# Input:    q - the candidate puzzle to validate
# Output:   boolean - whether or not the puzzle is valid
###
def valid(q):
	for i in range(3):
		for j in range(9):
			if len(get_knowns(q[i][j])) is not len(set(get_knowns(q[i][j]))):
				return False
	return True


###
# Function: get_knowns
# Purpose:  gets the known values(1 candidate) of a group
# Input:    group - the group to check the knowns for
# Output:   the set of elements from the group with a length of 1
###
def get_knowns(group):
	return [x[0] for x in group if len(x) is 1]

###
# Function: solved()
# Purpose:  checks if a candidate puzzle is solved
# Input:    q - candidate puzzle to check
# Output:   boolean - whether or not the puzzle is solved
###
def solved(q):
	for i in q:
		for c in i:
			for d in c:
				if len(d) > 1:
					return False
	return True