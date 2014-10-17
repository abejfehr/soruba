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

import copy #for the photocopy method

###
# Function: solve_sudoku()
# Purpose:  kicks off the sudoku solving process
# Input:    p - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   the completed puzzle - an 81 character string of numbers
###
def solve_sudoku(p):
	q = generate_candidate_puzzle(p)
	return solve(q)

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
	for i in range(81):
		if len(q[i]) is 1:
			clear_candidates(i, q)

	h = 2
	while(not solved(q) and h < 8):
		#solve the squares with > 1 possibility
		for i in range(81):
			if len(q[i]) is h:
				for j in range(h):
					nq = photocopy_puzzle_with(j, i, q)
					result = solve(nq)
					if result:
						return result
				return False
		h += 1

	if solved(q): return textify(q)
	return False

###
# Function: textify()
# Purpose:  Returns the string representation of the puzzle
# Input:    q - the candidate puzzle to textify
# Output:   an 81-character long string where the unknowns are periods
###
def textify(q):
	s = []
	for i in range(81):
		if len(q[i]) > 1: s.append(".")
		else: s.append(str(q[i][0]))
	s = "".join(s)
	return s

###
# Function: photocopy_puzzle_with()
# Purpose:  returns a copy of the candidate puzzle q, where the ith cell is
#						given the nth candidate's value
# Input:    n - the index of which candidate to take
#						i - the index of which cell to guess on
#						q - the candidate puzzle to copy
# Output:   the completed puzzle - the copy where the nth candidate of the ith
# 					cell is chosen.
###
def photocopy_puzzle_with(n, i, q):
	x = copy.deepcopy(q)
	x[i] = [x[i][n]]
	clear_candidates(i, x)
	return x

###
# Function: generate_candidate_puzzle()
# Purpose:  converts a string representation of a puzzle to a list of numbers
# Input:    puzzle - an 81 character string which is a sudoku puzzle.
#           Completed numbers are written and empty spaces are .'s
# Output:   candidate puzzle - the list that contains lists of candidates
###
def generate_candidate_puzzle(p):
	#the puzzle is already solved or isn't the correct length
	if not "." in p or len(p) is not 81: return False
	q = []
	for i in range(81):
		z = get_candidates(i, p)
		if z: q.append(z)
		else: return False
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
# Function: get_row_set()
# Purpose:  returns a set of the known values from the row of the ith cell
# Input:    i - the index of the cell whose row to get knowns from
#						q - the candidate puzzle to use
# Output:   the set of the known values from the row of the ith cell
###
def get_row_set(i, p):
	return map(int, [x for x in p[i/9*9:i/9*9+9] if x is not "."])

###
# Function: get_col_set()
# Purpose:  returns a set of the known values from the column of the ith cell
# Input:    i - the index of the cell whose column to get knowns from
#						q - the candidate puzzle to use
# Output:   the set of the known values from the column of the ith cell
###
def get_col_set(i, p):
	return map(int, [i%9 for x in p[i%9::9] if x is not "."])

###
# Function: get_box_set()
# Purpose:  returns a set of the known values from the box of the ith cell
# Input:    i - the index of the cell whose box to get knowns from
#						q - the candidate puzzle to use
# Output:   the set of the known values from the box of the ith cell
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
	if len(q[i]) > 1: return
	flag = False
	z = i / 9;
	for x in range(9):
		if q[i][0] in q[9*z+x] and 9*z+x is not i and len(q[9*z+x]) > 1:
			q[9*z+x].remove(q[i][0])
			flag = True
			if len(q[9*z+x]) is 1:
				clear_candidates(9*z+x, q)
	z = i % 9;
	for x in range(9):
		if q[i][0] in q[9*x+z] and 9*x+z is not i and len(q[9*x+z]) > 1:
			q[9*x+z].remove(q[i][0])
			flag = True
			if len(q[9*x+z]) is 1:
				clear_candidates(9*x+z, q)
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
	q = textify(q)
	for i in range(81):
		if len(get_row_set(i, q)) is not len(set(get_row_set(i, q))):
			return False
		if len(get_col_set(i, q)) is not len(set(get_col_set(i, q))):
			return False
		if len(get_box_set(i, q)) is not len(set(get_box_set(i, q))):
			return False
	return True

###
# Function: solved()
# Purpose:  checks if a candidate puzzle is solved
# Input:    q - candidate puzzle to check
# Output:   boolean - whether or not the puzzle is solved
###
def solved(q):
	for c in q:
		if len(c) > 1:
			return False
	return True
