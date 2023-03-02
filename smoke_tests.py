import unittest

from ScrambleSquareSolver import ScrambleSquare, solve_scramble

class TestStringMethods(unittest.TestCase):
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
        solutions, calls = solve_scramble(cards, verbose=False)
        expected = {'471583260', '568471302'}
        self.assertEqual(len(solutions), 2)
        self.assertEqual(solutions, expected)

    def test_bird_puzzle(self):
        # + => head, - => body
        cardinal, oriole , blue, bunting = 1, 2, 3, 4
        cards = [
            [bunting, cardinal, blue, -blue],
            [oriole, bunting, -blue, cardinal],
            [-bunting, oriole, cardinal, -blue],
            [-cardinal, blue, -bunting, oriole],
            [-cardinal, -oriole, bunting, blue],
            [-cardinal, oriole, -blue, -bunting],
            [-bunting, blue, oriole, -oriole],
            [-blue, -bunting, -cardinal, -oriole],
            [cardinal, blue, -bunting, oriole]
        ]
        solutions, calls = solve_scramble(cards, verbose=False)
        expected ={'480651327'}
        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions, expected)

    def test_planets_puzzle(self):
        # + => head, - => body
        earth, jupiter, saturn, mars = 1, 2, 3, 4
        cards = [
            [saturn, mars, saturn, -mars],
            [jupiter, -jupiter, earth, saturn],
            [saturn, -mars, jupiter, earth],
            [saturn, -mars, -jupiter, earth],
            [-mars, -earth, saturn, -mars],
            [-earth, -saturn, saturn, earth],
            [jupiter, earth, -jupiter, -mars],
            [jupiter, mars, saturn, earth],
            [-saturn, jupiter, -mars, mars]
        ]
        solutions, calls = solve_scramble(cards, verbose=False)
        expected = set()
        self.assertEqual(len(solutions), 0)
        self.assertEqual(solutions, expected)

    def test_africa_puzzle(self):
        # + => head, - => body
        elephant, zebra, giraffe, rhino = 1, 2, 3, 4
        cards = [
            [elephant, -zebra, -rhino, giraffe],
            [-elephant, -zebra, rhino, -giraffe],
            [elephant, giraffe, -rhino, zebra],
            [-zebra, -elephant, -giraffe, rhino],
            [-rhino, zebra, -giraffe, -elephant],
            [rhino, -giraffe, -elephant, -zebra],
            [-rhino, -zebra, rhino, -elephant],
            [rhino, -giraffe, elephant, giraffe],
            [zebra, -elephant, giraffe, -zebra]
        ]
        solutions, calls = solve_scramble(cards, verbose=False)
        expected = {'230145786', '230541786'}
        self.assertEqual(len(solutions), 2)
        self.assertEqual(solutions, expected)

    def test_plant_puzzle(self):
        cactus, aloe, paddle, heart = 1, 2, 3, 4
        # + => leaves, - => pot
        cards = [
            [-aloe, -cactus, +heart, +paddle],
            [-paddle, -aloe, +heart, +cactus],
            [-paddle, -heart, +cactus, +aloe],
            [-heart, -paddle, +cactus, +aloe],
            [-heart, -aloe, +cactus, +paddle],
            [-cactus, -paddle, +heart, +aloe],
            [-cactus, -paddle, +heart, +aloe],
            [-cactus, -aloe, +cactus, +paddle],
            [-heart, -paddle, +heart, +aloe]
        ]   
        solutions, calls = solve_scramble(cards, verbose=False)
        expected = {'458763012', '468753012'}
        self.assertEqual(len(solutions), 2)
        self.assertEqual(solutions, expected)

    
if __name__ == '__main__':
    unittest.main()