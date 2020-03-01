import unittest
from vrectangle import Vrectangle
from fractions import Fraction as _F

class TestVrectangle(unittest.TestCase):
    def setUp(self):
        # theoretically equivalent definitions for 5 vrectangles
        def1 = [
            Vrectangle(_F(1, 6), _F(1, 5), _F(4, 6), _F(4, 5), None),
            Vrectangle(_F(1, 6), _F(1, 5), _F(4, 6), _F(2, 5), None),
            Vrectangle(_F(1, 6), _F(2, 5), _F(3, 6), _F(4, 5), None),
            Vrectangle(_F(3, 6), _F(2, 5), _F(4, 6), _F(4, 5), None),
            Vrectangle(0, _F(3, 5), _F(2, 6), 1, None)
        ]
        def2 = [
            Vrectangle(0, 0, 1, 1, def1[0]),
            Vrectangle(0, 0, 1, _F(1, 3), def1[0]),
            Vrectangle(0, _F(1, 3), _F(2, 3), 1, def1[0]),
            Vrectangle(_F(2, 3), _F(1, 3), 1, 1, def1[0]),
            Vrectangle(-_F(1, 3), _F(2, 3), _F(1, 3), _F(4, 3), def1[0])
        ]
        def3 = [
            Vrectangle(0, -_F(1, 2), _F(3, 2), 1, def1[2]),
            Vrectangle(0, -_F(1, 2), _F(3, 2), 0, def1[2]),
            Vrectangle(0, 0, 1, 1, def1[2]),
            Vrectangle(1, 0, _F(3, 2), 1, def1[2]),
            Vrectangle(-_F(1, 2), _F(1, 2), _F(1, 2), _F(3, 2), def1[2])
        ]
        self.vrectangles = [def1, def2, def3]

    def test_equality(self):
        for defs1 in self.vrectangles:
            for defs2 in self.vrectangles:
                for def1, def2 in zip(defs1, defs2):
                    self.assertEqual(def1, def2)

if __name__ == '__main__':
    unittest.main()
