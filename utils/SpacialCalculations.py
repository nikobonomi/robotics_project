# se la linea può intersecare un'altra
from math import sqrt

import numpy as np


def can_intersect(line, target_line):
    return True


def line_intersection(line1, line2):
    x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div

    # verifico se il punto è davvero sui due segmenti. calcolo abbastanza semplice

    if np.abs((distance([line1[0], [x, y]]) + distance([[x, y], line1[1]])) - distance(line1))< 0.01 and \
            np.abs((distance([line2[0], [x, y]]) + distance([[x, y], line2[1]])) - distance(line2))< 0.01:
        return x, y

    return None


def distance(points):
    return sqrt(pow((points[1][0] - points[0][0]), 2) +
                pow((points[1][1] - points[0][1]), 2))
