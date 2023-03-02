import unittest
from collections import Counter

from ScrambleSquareSolver import ScrambleSquare, solve_scramble

class TestUnique(unittest.TestCase):
    def test_monkey_puzzle(self):
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
        unique = ScrambleSquare.find_unique(cards)
        self.assertEqual(len(set(unique)), 9)

    def test_repeat_puzzle(self):
        # + => head, - => body
        red, green = 1, 2
        cards = [
            [-green, -red, green, red],
            [-green, -red, green, red],
            [-green, -green, green, red],
            [-green, -red, green, red],
            [-green, -red, green, red],
            [-green, -red, green, red],
            [-green, red, red, -green],
            [-green, red, red, -red],
            [-green, red, red, -red]
        ]
        
        unique = ScrambleSquare.find_unique(cards)
        self.assertEqual(len(set(unique)), 4) 

        counts = Counter(unique)
        sorted_counts = sorted(counts.values())
        self.assertEqual(sorted_counts, [1, 1, 2, 5]) 

    def test_all_same(self):
        # + => head, - => body
        red, green = 1, 2
        green = red
        cards = [
            [-green, -red, green, red],
            [-green, -red, green, red],
            [-green, -green, green, red],
            [-green, -red, green, red],
            [-green, -red, green, red],
            [-green, -red, green, red],
            [-green, red, red, -green],
            [-green, red, red, -red],
            [-green, red, red, -red]
        ]
        
        unique = ScrambleSquare.find_unique(cards)
        self.assertEqual(len(set(unique)), 1) 
    
if __name__ == '__main__':
    unittest.main()