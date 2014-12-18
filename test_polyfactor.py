#!/usr/bin/env python3

import polyfactor
import unittest


class TestCoefficientsToEquation(unittest.TestCase):
    def test(self):
        self.assertEqual(polyfactor.coefficients_to_string([]), "")
        self.assertEqual(polyfactor.coefficients_to_string([0]), "0")
        self.assertEqual(polyfactor.coefficients_to_string([1]), "1")
        self.assertEqual(
            polyfactor.coefficients_to_string([1, 2, 3]), "3x^2 + 2x + 1")
        self.assertEqual(
            polyfactor.coefficients_to_string([-1, 0, 3]), "3x^2 - 1"
        )
        self.assertEqual(
            polyfactor.coefficients_to_string([0, 0, -2]), "-2x^2"
        )


class TestFindFactors(unittest.TestCase):
    def test(self):
        self.assertEqual(polyfactor.find_factors(0), [])
        self.assertEqual(polyfactor.find_factors(1), [1])
        self.assertEqual(polyfactor.find_factors(2), [1, 2])
        self.assertEqual(polyfactor.find_factors(3), [1, 3])
        self.assertEqual(polyfactor.find_factors(4), [1, 2, 4])
        self.assertEqual(polyfactor.find_factors(-1), [1])
        self.assertEqual(polyfactor.find_factors(-2), [1, 2])
        self.assertEqual(polyfactor.find_factors(-3), [1, 3])
        self.assertEqual(polyfactor.find_factors(-4), [1, 2, 4])
        self.assertEqual(
            polyfactor.find_factors(30),
            [1, 2, 3, 5, 6, 10, 15, 30]
        )


class TestEvaluateFunc(unittest.TestCase):
    def test(self):
        # f(x) = -99
        self.assertEqual(polyfactor.evaluate_func([-99], 1), -99)
        # f(x) = x - 99
        self.assertEqual(polyfactor.evaluate_func([0, 1], -99), -99)
        # f(x) = x^2 + x + 1
        self.assertEqual(polyfactor.evaluate_func([1, 1, 1], 0), 1)
        self.assertEqual(polyfactor.evaluate_func([1, 1, 1], 2), 7)
        self.assertEqual(polyfactor.evaluate_func([1, 1, 1], -2), 3)
        # f(x) = x^2
        self.assertEqual(polyfactor.evaluate_func([0, 0, 1], 0), 0)
        self.assertEqual(polyfactor.evaluate_func([0, 0, 1], -1), 1)
        self.assertEqual(polyfactor.evaluate_func([0, 0, 1], -2), 4)


class TestFindPossibleRoots(unittest.TestCase):
    def test(self):
        self.assertEqual(polyfactor.find_possible_roots([-99]), [])
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([1, 1])),
            [-1.0, 1.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([1, 2])),
            [-1.0, -0.5, 0.5, 1.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([2, 1])),
            [-2.0, -1.0, 1.0, 2.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([4, 1])),
            [-4.0, -2.0, -1.0, 1.0, 2.0, 4.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([3, 2])),
            [-3.0, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 3.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([0, 1, 2])),
            [-1.0, -0.5, 0.5, 1.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([0, -99])),
            [0.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_possible_roots([0, 0, -99])),
            [0.0]
        )


class TestFindRationalRoots(unittest.TestCase):
    def test(self):
        self.assertEqual(polyfactor.find_rational_roots([-99]), [])
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([1, 1])),
            [-1.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([1, 2])),
            [-0.5]
        )
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([-2, 1])),
            [2.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([4, 1])),
            [-4.0]
        )
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([3, 2])),
            [-1.5]
        )
        # (x+3)(x-2) = x^2 + x - 6
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([-6, 1, 1])),
            [-3.0, 2.0]
        )
        # (x+3)(2x+1)(x-2) = 2x^3 + 3x^2 - 11x - 6
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([-6, -11, 3, 2])),
            [-3.0, -0.5, 2.0]
        )
        # (x+1)^4
        self.assertEqual(
            sorted(polyfactor.find_rational_roots([1, 4, 6, 4, 1])),
            [-1.0]
        )
        # (x+7)(x+5)(x-1)(4x-5)(x-3)
        self.assertEqual(
            sorted(
                polyfactor.find_rational_roots([-525, 940, -366, -80, 27, 4])
            ),
            [-7.0, -5.0, 1.0, 1.25, 3.0]
        )


class TestFactorEquation(unittest.TestCase):
    def test(self):
        self.assertEqual(
            polyfactor.factor_equation([1, 1]),
            ([-1.0], 1.0)
        )
        self.assertEqual(
            polyfactor.factor_equation([1, 2, 1]),
            ([-1.0, -1.0], 1.0)
        )
        self.assertEqual(
            polyfactor.factor_equation([1, 3, 3, 1]),
            ([-1.0, -1.0, -1.0], 1.0)
        )
        self.assertEqual(
            polyfactor.factor_equation([-1, 0, 1]),
            ([-1.0, 1.0], 1.0)
        )
        self.assertEqual(
            polyfactor.factor_equation([-1, -1, 2]),
            ([-0.5, 1.0], 2.0)
        )
        self.assertEqual(
            polyfactor.factor_equation([16, -16, 4]),
            ([2.0, 2.0], 4.0)
        )
        # (x+7)(x+5)(x-1)(4x-5)(x-3)
        self.assertEqual(
            polyfactor.factor_equation([-525, 940, -366, -80, 27, 4]),
            ([-7.0, -5.0, 1.0, 1.25, 3.0], 4.0)
        )
        # (x+1)^3(x-1)^2(4x-5)(x-3)
        self.assertEqual(
            polyfactor.factor_equation([15, -2, -43, 8, 41, -10, -13, 4]),
            ([-1.0, -1.0, -1.0, 1.0, 1.0, 1.25, 3.0], 4.0)
        )


class TestFactoredEquationToString(unittest.TestCase):
    def test(self):
        self.assertEqual(
            polyfactor.factored_equation_to_string(([-1.0], 1.0)),
            "(x+1)"
        )
        self.assertEqual(
            polyfactor.factored_equation_to_string(([-1.0, -1.0], 1.0)),
            "(x+1)^2"
        )
        self.assertEqual(
            polyfactor.factored_equation_to_string(([-1.0, -1.0, -1.0], 1.0)),
            "(x+1)^3"
        )
        self.assertEqual(
            polyfactor.factored_equation_to_string(
                ([-1.0, -1.0, -1.0, -1.0], 1.0)
            ),
            "(x+1)^4"
        )
        self.assertEqual(
            polyfactor.factored_equation_to_string(([-1.0, 1.0], 1.0)),
            "(x+1)(x-1)"
        )
        self.assertEqual(
            polyfactor.factored_equation_to_string(([-0.5, 1.0], 1.0)),
            "(x+0.5)(x-1)"
        )
        self.assertEqual(
            polyfactor.factored_equation_to_string(
                ([-7.0, -5.0, 1.0, 1.25, 3.0], 1.0)
            ),
            "(x+7)(x+5)(x-1)(x-1.25)(x-3)"
        )
        self.assertEqual(
            polyfactor.factored_equation_to_string(
                ([-1.0, -1.0, -1.0, 1.0, 1.0, 1.25, 3.0], 1.0)
            ),
            "(x+1)^3(x-1)^2(x-1.25)(x-3)"
        )

if __name__ == '__main__':
    unittest.main()
