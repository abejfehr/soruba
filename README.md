Soruba
======

The Soruba project was something that I decided to do for fun in third year. The main goal of the project was to create a piece of code that could solve sudoku puzzles with accuracy.

The name **soruba** comes from the Japanese word for *solver*.

Instructions
============

To use the solver, simply import everything into your project and call `solve_sudoku(puzzle)`, where `puzzle` is a sudoku formatted as an 81 character long string with periods for blank spaces.

**Warning: ** The solver will likely fail when presented with a malformed string, or anything that's not a sudoku puzzle. Since this was intended to be a proof-of-concept, the [fail-gracefully-principle](https://en.wikipedia.org/wiki/Graceful_exit) hasn't yet been implemented.

###Testing

There are 2 lists of puzzles included in this repository, `easy_puzzles.txt` and `difficult_puzzles.txt`, aptly named for the level of puzzles they contain.