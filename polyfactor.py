#!/usr/bin/env python3

"""
Factor and plot polynomials.
"""

# http://www.mathportal.org/calculators/polynomials-solvers/

import math
import matplotlib.pyplot  # sudo apt-get install python3-matplotlib


def coefficients_to_string(coefficients):
    """Convert coefficients to a human-readable string."""
    if len(coefficients) == 1:
        equation = str(coefficients[0])
    else:
        equation = ""
        for index, coefficient in enumerate(coefficients):
            if coefficient != 0:
                # Add the x^n part.
                if index == 1:
                    equation = "x" + equation
                elif index >= 2:
                    equation = "x^{}{}".format(index, equation)

                # Determine the sign character.
                if index == len(coefficients) - 1:
                    if coefficient < 0:
                        sign = "-"
                    else:
                        sign = ""
                else:
                    if coefficient < 0:
                        sign = " - "
                    else:
                        sign = " + "

                # Add the sign and the coefficient.
                coefficient = abs(coefficient)
                if coefficient == 1 and index > 0:
                    coefficient = ""
                equation = "{}{}{}".format(sign, coefficient, equation)

    return equation


def factored_equation_to_string(factored_equation):
    """Convert factors to a human-readable string."""
    factors, remainder = factored_equation
    factors = sorted(factors)
    if remainder == 1.0:
        string = ""
    else:
        string = "{:g}".format(remainder)
    index = 0
    while index < len(factors):
        string += "(x{}{:g})".format(
            "+" if factors[index] < 0.0 else "-",
            abs(factors[index])
        )
        count = 1
        while (
            index + count < len(factors) and
            factors[index] == factors[index + count]
        ):
            count += 1
        if count > 1:
            string += "^{}".format(count)
        index += count

    return string


def find_factors(num):
    """Calculate integer factors of num."""
    num = abs(num)
    factor = math.floor(math.sqrt(num))
    factors = []
    while factor > 0:
        if num % factor == 0:
            factors.insert(0, factor)
            other_factor = num // factor
            if other_factor != factor:
                factors.append(other_factor)
        factor -= 1
    return factors


def evaluate_func(coefficients, x):
    """Evaluate the f(x)."""
    x_pow = 1
    y = 0
    for coefficient in coefficients:
        y += coefficient * x_pow
        x_pow *= x
    return y


def find_possible_roots(coefficients):
    """Calculate all possible integer roots of an equation."""
    if len(coefficients) <= 1:
        return []
    # Find the last non-zero coefficient.
    last_coefficient = None
    for index, coefficient in enumerate(coefficients):
        if coefficient != 0.0:
            if index == len(coefficients) - 1:
                return [0.0]
            last_coefficient = coefficient
            break
    possible_roots = []
    if last_coefficient is not None:
        first_term_factors = find_factors(coefficients[-1])
        last_term_factors = find_factors(last_coefficient)
        for first_term_factor in first_term_factors:
            for last_term_factor in last_term_factors:
                root = last_term_factor / first_term_factor
                if root not in possible_roots:
                    possible_roots.append(root)
                    possible_roots.append(-root)
    return possible_roots


def find_rational_roots(coefficients):
    """Calculate all rational roots of an equation."""
    possible_roots = find_possible_roots(coefficients)
    rational_roots = []
    for possible_root in possible_roots:
        if evaluate_func(coefficients, possible_root) == 0:
            rational_roots.append(possible_root)
    return rational_roots


def divide(coefficients, root):
    """Try to divide the equation by the root.  Return result if
    successful or None if there was a remainder."""
    remainder = 0.0
    new_coefficients = []
    for coefficient in reversed(coefficients):
        remainder = root * remainder + coefficient
        new_coefficients.insert(0, remainder)
    return new_coefficients[1:] if remainder == 0.0 else None


def factor_equation(coefficients):
    """Factor an equation returning a list of factors and the
    multiplicative remainder."""
    roots = find_rational_roots(coefficients)
    factors = []

    for root in roots:
        while True:
            new_coefficients = divide(coefficients, root)
            if new_coefficients is None:
                break
            factors.append(root)
            coefficients = new_coefficients

    # Even though there is no order to factors, it is easier to test
    # if we return them sorted.
    factors = sorted(factors)
    return factors, coefficients[0]


def determine_domain(roots):
    """Determine the domain (min/max X values) for a nice plot."""
    x_min = min(roots)
    x_max = max(roots)

    # Grow the domain by +-10%, but at least by 1.
    x_delta = max((x_max - x_min) / 10.0, 0.5)
    x_min -= x_delta
    x_max += x_delta

    # Grow domain equally on either side until the domain includes the origin.
    grow_left = max(0.0, x_min + 1.0)
    grow_right = max(0.0, 1.0 - x_max)
    grow = max(grow_left, grow_right)
    x_min -= grow
    x_max += grow

    return (x_min, x_max)


def generate_points(coefficients, domain):
    """Generate graph points for an equation."""
    n_points = 400
    x_delta = (domain[1] - domain[0]) / (n_points - 1)
    x_values = []
    y_values = []
    for i in range(n_points):
        x = domain[0] + i * x_delta
        y = evaluate_func(coefficients, x)
        x_values.append(x)
        y_values.append(y)
    return (x_values, y_values)


def plot_equation(axis, coefficients):
    """Plot an equation on a Axis."""

    # Find the roots of the equation.
    roots = find_rational_roots(coefficients)

    # Plot the roots as blue circles.
    y_values = [0.0 for _ in roots]
    axis.plot(roots, y_values, "bo")

    # Plot the equation.
    domain = determine_domain(roots)
    x_values, y_values = generate_points(coefficients, domain)
    axis.plot(x_values, y_values)

    # Display a coordinate grid and highlight the axes.
    axis.grid(True)
    axis.axhline(0, color='black', lw=2)
    axis.axvline(0, color='black', lw=2)

    title = "{}\n{}".format(
        coefficients_to_string(coefficients),
        factored_equation_to_string(factor_equation(coefficients))
    )
    axis.set_title(title)


def main():
    """main"""
    # Create a list of subplots (axes).
    fig, axes = matplotlib.pyplot.subplots(2, 2)

    # Plot equations.
    plot_equation(axes[0][0], [-6, 1, 1])
    plot_equation(axes[0][1], [16, -16, 4])
#    plot_equation(axes[0][1], [1, 4, 6, 4, 1])
    # (x+3)(2x+1)(x-2)
    plot_equation(axes[1][0], [-6, -11, 3, 2])
    # (x+7)(x+5)(x-1)(4x-5)(x-3)
    plot_equation(axes[1][1], [-525, 940, -366, -80, 27, 4])

    # Show the plot.
    fig.tight_layout()
    matplotlib.pyplot.show()


if __name__ == "__main__":
    main()
