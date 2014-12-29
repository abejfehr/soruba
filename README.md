Soruba
======

Soruba is a Sudoku solver written in *Python*.

The main goal of the project was to create a piece of code that could solve sudoku puzzles with accuracy, and *some* level of efficiency.

The name **soruba** comes from the Japanese word for *solver*.

Instructions
============

To use the solver, simply import everything into your project and call `solve_sudoku(puzzle)`, where `puzzle` is a sudoku formatted as an 81 character long string with periods for blank spaces, like so:

`5...68..........6..42.5.......8..9....1....4.9.3...62.7....1..9..42....3.8.......`

**Warning: ** The solver will likely fail when presented with a malformed string, or anything that's not a sudoku puzzle. Since this was intended to be a proof-of-concept, the [fail-gracefully-principle](https://en.wikipedia.org/wiki/Graceful_exit) hasn't yet been implemented.

Testing
-------

There are 2 lists of puzzles included in this repository, `easy_puzzles.txt` and `difficult_puzzles.txt`, appropriately named for the difficulty level of the puzzles they contain.
