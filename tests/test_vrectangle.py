import unittest
from vrectangle import Vrectangle
from fractions import Fraction

class TestVrectangle(unittest.TestCase):
    def setUp(self):
        xth = lambda x: Fraction(1, x)
        # theoretically equivalent definitions for 5 vrectangles
        def1 = [
            Vrectangle(xth(6), xth(5), 4 * xth(6), 4 * xth(5), None),
            Vrectangle(xth(6), xth(5), 4 * xth(6), 2 * xth(5), None),
            Vrectangle(xth(6), 2 * xth(5), 3 * xth(6), 4 * xth(5), None),
            Vrectangle(3 * xth(6), 2 * xth(5), 4 * xth(6), 4 * xth(5), None),
            Vrectangle(0, 3 * xth(5), 2 * xth(6), 1, None)
        ]
        def2 = [
            Vrectangle(0, 0, 1, 1, def1[0]),
            Vrectangle(0, 0, 1, xth(3), def1[0]),
            Vrectangle(0, xth(3), 2 * xth(3), 1, def1[0]),
            Vrectangle(2 * xth(3), xth(3), 1, 1, def1[0]),
            Vrectangle(-xth(3), 2 * xth(3), xth(3), 4 * xth(3), def1[0])
        ]
        def3 = [
            Vrectangle(0, -xth(2), 3 * xth(2), 1, def1[2]),
            Vrectangle(0, -xth(2), 3 * xth(2), 0, def1[2]),
            Vrectangle(0, 0, 1, 1, def1[2]),
            Vrectangle(1, 0, 3 * xth(2), 1, def1[2]),
            Vrectangle(-xth(2), xth(2), xth(2), 3 * xth(2), def1[2])
        ]
        self.vrectangles = [def1, def2, def3]

    def test_equality(self):
        for defs1 in self.vrectangles:
            for defs2 in self.vrectangles:
                for def1, def2 in zip(defs1, defs2):
                    self.assertEqual(def1, def2)

if __name__ == '__main__':
    unittest.main()
