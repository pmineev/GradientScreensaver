from math import pi, sin


def linear(a, b, k):
    return a * (1.0 - k) + b * k


def sine(a, b, k):
    return linear(a, b, sin(pi / 2 * k))


def cubic_bezier(a, b, k):
    p = [0.0, 0.5, 0.5, 1.0]
    return linear(a, b,
                  (1 - k) ** 3 * p[0] + 3 * k * (1 - k) ** 2 * p[1] + 3 * k ** 2 * (1 - k) * p[2] + k ** 3 * p[3])
