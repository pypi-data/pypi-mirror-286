import unittest
from puzzle_py import PuzzleCore

class MyTestCase(unittest.TestCase):
    def test_something(self):
        pz = PuzzleCore(3)
        # set 0 to top
        pz.move_sequence('UU')

        pz1 = pz.get_puzzle()
        pz.move_sequence('DD')
        pz.move_sequence('uu')
        pz2 = pz.get_puzzle()

        self.assertEqual(pz1, pz2)  # add assertion here


if __name__ == '__main__':
    unittest.main()
