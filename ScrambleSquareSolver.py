"""
ScrambleSquareSolver.py

Lior Sinai
10 March 2017

Solves scramble square puzzles
Algorithm from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.953.6583&rep=rep1&type=pdf
9 different positions for each card * 4 orientations for each except for the middle because that only rotates the whole board
 = 9!*(4**8) = 23781703680 ~= 23.8 billion combinations
 
              
Rotation:            0         1       2       3              
                     0         3       2       1
Card = [0 1 2 3]   3   1     2   0   1   3   0   2
                     2         1       0       3

Fitting condition:
Let card1=[a, b, c, d] and card2=[e, f, g, h], then the cards 'fit' if card1[x] + card2[y] = 0
where x=side1-rot1 where side1 and rot1 in (0, 1, 2, 3).
and similarly for y.

        6 7 8
Board:  5 0 1   Start at k=0 in the centre, and place cards in a clockwise spiral for k=1,2,...,8.
        4 3 2

"""

from datetime import datetime
from copy import copy, copy
from typing import List, Set

SIZE = 9
NUM_ORIENTATIONS = 4


class ScrambleSquare():
    def __init__(self, pieces):
        self.pieces = pieces
        self.order = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.rotation = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.unique = ScrambleSquare.find_unique(pieces)

    def __repr__(self):
        repr = ''
        order = self.order
        repr += ' '.join(map(str, [order[6], order[7], order[8]])) + '\n'
        repr += ' '.join(map(str, [order[5], order[0], order[1]])) + '\n'
        repr += ' '.join(map(str, [order[4], order[3], order[2]]))
        return repr

    def fit_2_pieces(self, piece1: List[int], rot1: int, side1: int,
                     piece2: List[int], rot2: int, side2: int) -> bool:
        "Checks if 2 pieces at 2 specific orientations fit together"
        return piece1[side1 - rot1] + piece2[side2 - rot2] == 0

    def fit_position(self, k: int, used_k: int, rot_k: int) -> bool:
        "Checks the fit of a piece at a specific position k on the board"
        if k == 0:
            fits = True
        else:  # Each piece must fit with the previous card:
            piece_k = self.pieces[used_k]
            side_k = [1, 3, 0, 1, 1, 2, 2, 3, 3][k]
            piece_j = self.pieces[self.order[k - 1]]
            rot_j = self.rotation[k - 1]
            side_j = [0, 1, 2, 3][side_k - 2]  # picks the opposite side
            fits = self.fit_2_pieces(
                piece_k, rot_k, side_k, piece_j, rot_j, side_j)

        # Extra fitting criteria for particular positions:
        if k in [3, 5, 7, 8]:
            pieces, order, rot = self.pieces, self.order, self.rotation
            if k == 3:
                side_k = 0
                piece_other, rot_other, side_other = pieces[order[0]], rot[0], 2
            elif k == 5:
                side_k = 1
                piece_other, rot_other, side_other = pieces[order[0]], rot[0], 3
            elif k == 7:
                side_k = 2
                piece_other, rot_other, side_other = pieces[order[0]], rot[0], 0
            elif k == 8:
                side_k = 2
                piece_other, rot_other, side_other = pieces[order[1]], rot[1], 0
            fits = fits and self.fit_2_pieces(
                piece_k, rot_k, side_k, piece_other, rot_other, side_other)
        return fits
    
    def rotation_mapping(self):
        "A mapping of piece idx to rotation. Assumes every piece is unique"
        orientations = dict()
        for i in range(0, len(self.order)):
            if self.order[i] == -1:
                continue
            orientations[self.order[i]] = self.rotation[i]
        return orientations
    
    @staticmethod
    def find_unique(pieces):
        seen = dict()
        unique = [-1] * len(pieces)
        hash_const = 2 * abs_max_matrix(pieces) + 1
        for i in range(0, len(pieces)):
            is_unique = True
            for r in range(NUM_ORIENTATIONS):
                piece_r = pieces[i][r:] + pieces[i][:r]
                key = ScrambleSquare.hash(piece_r, n=hash_const)
                if key in seen:
                    is_unique = False
                    break
            if is_unique:
                seen[key] = i
            unique[i] = seen[key]
        return unique
    
    @staticmethod
    def hash(piece, n=10):
        # for each number to map to a unique positive number require n>=2*max(abs(value))+1
        hash = ''.join(str(x % n) for x in piece)
        return hash
    

def abs_max_matrix(matrix):
    return max([max([abs(x) for x in row]) for row in matrix])


def solve_scramble(pieces: List[int], check_repeats=False, verbose=True) -> None:
    def solve(k: int, puzzle, stack: List[int], history: Set=set()):
        calls[k] += 1
        if k == SIZE:
            solution = [str(x) if x != -1 else '-' for x in puzzle.order]
            solution_str = ''.join(solution)
            if check_repeats and solution_str in solutions:
                return
            solutions.add(solution_str)
            if verbose:
                print_solution(puzzle, calls)
            return
        for idx in range(len(stack)):
            # select a new piece that hasn't been used
            new = stack[idx]
            if check_repeats:
                new = puzzle.unique[new]
            # try different orientations of that piece
            for r in range(NUM_ORIENTATIONS):
                if check_repeats and (k, new, r) in history:
                    if k == 0: # equivalent: go to the last clause in the for loop
                        break 
                    continue
                history.add((k, new, r))
                if puzzle.fit_position(k, new, r):
                    # go on to the next position on the board
                    # use recursion to implement a backtracking algorithm:
                    puzzle_next = copy(puzzle)
                    history_next = copy(history)
                    puzzle_next.order[k] = new
                    puzzle_next.rotation[k] = r
                    stack_next = stack[:idx] + stack[idx + 1:]
                    solve(k + 1, puzzle_next, stack_next, history=history_next)
                if k == 0:
                    break  # don't rotate the first piece

    # stores calls of solve_scramble() at each level = number of solutions at each level
    calls = [0] * (SIZE + 1)
    stack = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    puzzle = ScrambleSquare(pieces)
    solutions = set()

    solve(0, puzzle, stack, set())

    return solutions, calls


def print_solution(puzzle, calls, check_repeats=False):
    print('Solution found!!')
    print(puzzle)
    orientations = puzzle.rotation if check_repeats else puzzle.rotation_mapping()
    print('orientations: ', orientations)
    print('# calls =', sum(calls))
    print(' ')


def find_first(array, value):
    return next(iter(i for i in range(0, len(array)) if array[i] == value), None)


if __name__ == "__main__":
    startTime = datetime.now()
    # Monkey Puzzle
    # + => head, - => body
    blue, green, red, purple = 1, 2, 3, 4
    cards = [
        [-green, -red, +blue, +purple],
        [-purple, +blue, +purple, -green],
        [-blue, -green, +blue, +red],
        [-purple, +green, +red, -blue],
        [+red, -purple, -green, +purple],
        [-blue, -red, +green, +purple],
        [-red, +green, +red, -blue],
        [-green, -blue, +purple, +red],
        [-purple, -green, +red, +purple]
    ]

    solutions, calls = solve_scramble(cards, check_repeats=True, verbose=False)

    print('number of solutions =', len(solutions))
    print('total calls =', sum(calls))
    print('calls per position:', calls)

    print('Time taken:', datetime.now() - startTime)
