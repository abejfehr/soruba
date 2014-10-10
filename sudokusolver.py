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

## from now on, q will be a candidate puzzle as such that it contains [[rowset],
## [colset], [boxset]]

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
		for j in range(9)
			if len(q[0][i][j]) is 1:
				clear_candidates(i, q)

	h = 2
	while(not solved(q) and h < 8):
		#solve the squares with > 1 possibility
		for i in range(9):
			for j in range(9):
				if len(q[0][i][j]) is h:
					for k in range(h):
						nq = photocopy_puzzle_with(k, i*9+j, q)
	#					print textify(nq)
	#					print " " * i + "^"
	#					print " " * i + str(q[i])
	#					print valid(nq)
	#					raw_input("Press Enter to Continue")
						result = solve(nq)
						if result:
							return result
					return False
		h += 1

	if solved(q): return textify(q)
	return False

def solve2(q):
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
	for i in range(81):
		if len(q[i]) > 1: s.append(".")
		else: s.append(str(q[i][0]))
	s = "".join(s)
	return s

###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def photocopy_puzzle_with(n, i, q):
	x = copy.deepcopy(q)
	#convert the i to
	v = [x[0][i%9][i/9][n]]
	x[0][i%9][i/9][n] = v
	x[1][i/9][i%9][n] = v
	x[2][i/9*3+i%9][i/9%3*3+i%9%3][n] = v
	clear_candidates(i, x)
	return x

"""
x  i j
0  0 0  a = offset from the left edge of the puzzle = x % 9
1  0 1  j = offset from the left edge of the box = a % 3
2  0 2  b = offset from the top edge of the puzzle x / 9
3  1 0  i = offset from the top edge of the box = b % 3
4  1 1  k = 1 to 9 coordinate in the box = i * 3 + j
5  1 2  m = box coord from left = a / 3
6  2 0  n = box coord from top = b / 3
7  2 1  s = b * 3 + a
"""

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
		q.append([get_candidates(z*9+j,p) if x is "." else [int(x)] for (j,x) in enumerate(p[z*9:z*9+9])])
	return q

def get_candidate_cols(p):
	q = []
	for z in range(9):
		q.append([get_candidates(j*9+z,p) if x is "." else [int(x)] for (j,x) in enumerate(p[z::9])])
	return q

def get_candidate_boxes(p):
	q = []
	for m in [n for n in range(81) if n % 3 is 0 and (n / 9) % 3 is 0]:
		q.append([get_candidates(m+j%3+j/3*9,p) if x is "." else [int(x)] for (j,x) in enumerate(p[m:m+3] + p[m+9:m+12] + p[m+18:m+21])])
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
	row = get_row_set(i, p)
	col = get_col_set(i, p)
	box = get_box_set(i, p)
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
def get_row_set(i, p):
	z = i / 9
	return map(int, [x for x in p[z*9:z*9+9] if x is not "."])

###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def get_col_set(i, p):
	z = i % 9
	return map(int, [x for x in p[z::9] if x is not "."])

###
# Function: solve()
# Purpose:  solves a sudoku puzzle
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def get_box_set(i, p):
	m = 9 * (i / 9 / 3 * 3) + (i % 9 / 3 * 3)
	return map(int, [x for x in p[m:m+3] + p[m+9:m+12] + p[m+18:m+21] if x is not "."])

###
# Function: clear_candidates()
# Purpose:  clears all the numbers from the related cells of the puzzle
# Input:    i - the index of the cell whose neighbours to clear
#						q - the full candidate puzzle to clear from
# Output:   boolean - whether or not any candidates were cleared from the
#           related squares
###
def clear_candidates(i, q):

	if len(q[0][i%9][i/9]) > 1: return
	flag = False

	a = i%9
	b = i/9
	for w in range(2):
		for x in range(9):
			if q[w][a][b][0] in q[w][a][x] and i/9 is not x and len(q[w][a][x]) > 1:
				q[w][a][b].remove(q[w][a][b][0])
				flag = True
				if len(q[w][a][x]) is 1:
					clear_candidates(a*9+x, q)
		#switch a and b
		z = a; a = b; b = z
	for x in range(9):

	a = i/9*3+i%9
	b = i/9%3*3+i%9%3

	#TODO: make this work with the new q; this is the last thing I need to do before it's awesome
	m = 9 * (i / 9 / 3 * 3) + (i % 9 / 3 * 3)
	for x in range(3):
		for y in range(3):
			if q[i][0] in q[m+(x*9)+y] and m+(x*9)+y is not i and len(q[m+(x*9)+y]) > 1:
				q[m+(x*9)+y].remove(q[i][0])
				flag = True
				if len(q[m+(x*9)+y]) is 1:
					clear_candidates(m+(x*9)+y, q)
	return flag

###
# Function: valid()
# Purpose:  checks the validity of a candidate puzzle
# Input:    q - the candidate puzzle to validate
# Output:   boolean - whether or not the puzzle is valid
###
def valid(q):
	for i in range(3):
		for j in range(9):
			if(len(get_knowns(q[i][j])) is not len(set(get_knowns(q[i][j])))):
				return false
	return True


###
# Function: get_knowns
# Purpose:  gets the known values(1 candidate) of a group
# Input:    group - the group to check the knowns for
# Output:   the set of elements from the group with a length of 1
###
def get_knowns(group):
	return [x for x in group if len(x) is 1]

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
