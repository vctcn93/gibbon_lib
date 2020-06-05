import numpy as np


def distance_point_point(p1: np.ndarray, p2: np.ndarray) -> float:
    return abs(np.linalg.norm(p1 - p2))


def distance_point_segment(point, segment) -> float:
    return abs(
        np.cross(segment[1] - segment[0], point - segment[0]
        ) / np.linalg.norm(segment[1] - segment[0])
    )


def distance_point_polyline(point, polyline) -> float:
    segments = segments_of_polyline(polyline)
    return min(
        [distance_point_segment(point, segment) for segment in segments]
    )


def segments_of_polyline(polyline) -> list:
    return [
        [polyline[i], polyline[i+1]] for i in range(len(polyline) - 1)
    ]


def length_of_polyline(polyline) -> float:
    segments = segments_of_polyline(polyline)
    return sum([distance_point_point(segment[0], segment[1]) for segment in segments])


def point_at_parameter_segement(segment, param) -> np.ndarray:
    diss = segment[1] - segment[0]
    return segment[0] + param * diss


def point_at_parameter_polyline(polyline, param) -> np.ndarray:
    segments = segments_of_polyline(polyline)
    segment_lengths = [distance_point_point(segment[0], segment[1]) for segment in segments]
    entire_length = sum(segment_lengths)
    diss = param * entire_length

    def f(aim, lengths):
        for i in range(len(lengths)):
            if aim - lengths[i] <= 0:
                return [aim, i]
            else:
                aim -= lengths[i]

    aim, index = f(diss, segment_lengths)
    segment = [polyline[index], polyline[index+1]]
    length = distance_point_point(segment[0], segment[1])
    param = aim / length
    return point_at_parameter_segement(segment, param)


def is_point_in_segment_domian(point, segment, include_intersection=True) -> bool:
    roundoff = 6
    a, b = segment
    minx = round(min(a[0], b[0]), roundoff)
    maxx = round(max(a[0], b[0]), roundoff)
    miny = round(min(a[1], b[1]), roundoff)
    maxy = round(max(a[1], b[1]), roundoff)
    x = round(point[0], roundoff)
    y = round(point[1], roundoff)

    tolerance =0.00001

    if not include_intersection:
        if (abs(point[0] - segment[0][0]) < tolerance and abs(point[1] - segment[0][1]) < tolerance) or \
                (abs(point[0] - segment[1][0]) < tolerance and abs(point[1] - segment[1][1]) < tolerance):
            return False

    if x < minx or x > maxx:
        return False

    if y < miny or y > maxy:
        return False

    return True


def is_point_in_polyline(point, polyline) -> bool:
    counter = 0
    x, y, p1 = point[0], point[1], polyline[0]

    for p2 in polyline:
        if min([p1[0], p2[0]]) < x <= max([p1[0], p2[0]]):
            if y <= max([p1[1], p2[1]]):
                if p1[0] != p2[0]:
                    xinters = (x - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0]) + p1[1]
                    if p1[1] == p2[1] or y <= xinters:
                        counter += 1

        p1 = p2

    if counter % 2 == 0:
        return False
    else:
        return True


if __name__ == '__mian__':
    # distance_point_point
    p1, p2 = np.array([0, 0]), np.array([1, 1])
    distance = distance_point_point(p1, p2)
    assert distance - 1.4142135623730951 < .000001

    # distance_segment_point
    p = np.array([0, 5])
    segment = [np.array([0, 0]), np.array([10, 10])]
    distance = distance_point_segment(p, segment)
    assert distance - 3.5355339059327373 < .000001

    # segments_of_polyline
    polyline = [
        np.array([0, 0]),
        np.array([10, 10]),
        np.array([20, 8]),
        np.array([30, 25]),
        np.array([45, 30])
    ]
    segments = segments_of_polyline(polyline)
    assert segments == [
        [np.array([0, 0]), np.array([10, 10])],
        [np.array([10, 10]), np.array([20,  8])],
        [np.array([20,  8]), np.array([30, 25])],
        [np.array([30, 25]), np.array([45, 30])]
    ]

    # distance_polyline_point
    distance = distance_point_polyline(p, polyline)
    assert distance - 3.5355339059327373 < .000001

    # point_at_parameter_segement
    p = point_at_parameter_segement(segment, .5)
    assert p == np.array([5, 5])

    # point_at_parameter_polyline
    p = point_at_parameter_polyline(polyline, .3)
