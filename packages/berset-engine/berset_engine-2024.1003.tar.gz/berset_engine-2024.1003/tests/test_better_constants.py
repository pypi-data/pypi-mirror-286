import unittest
from berset_engine.better.constants import Constants

betterConstant = Constants()

class Test_better_constant(unittest.TestCase):
    def test_constant(self):
        self.assertEqual(
            betterConstant.M3_to_kWh,
            11.56,
            "not equals"
        )

if __name__=='__main__':
    unittest.main()

