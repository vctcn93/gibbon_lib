import numpy as np


def distance_point_point(p1: np.ndarray, p2: np.ndarray) -> float:
    return abs(np.linalg.norm(p1 - p2))


def distance_segment_point(segment, point) -> float:
    return abs(
        np.cross(segment[1] - segment[0], point - segment[0]
        ) / np.linalg.norm(segment[1] - segment[0])
    )


def distance_polyline_point(polyline, point) -> float:
    segments = segments_of_polyline(polyline)
    return min(
        [distance_segment_point(segment, point) for segment in segments]
    )


def segments_of_polyline(polyline) -> list:
    return [
        [polyline[i], polyline[i+1]] for i in range(len(polyline) - 1)
    ]


def length_of_polyline(polyline) -> float:
    segments = segments_of_polyline(polyline)
    return sum([distance_point_point(segment[0], segment[1]) for segment in segments])


def point_at_parameter_segement(segment, param):
    diss = segment[1] - segment[0]
    return segment[0] + param * diss


def point_at_parameter_polyline(polyline, param):
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


def is_in_polygon(point, polygon):
    pass


if __name__ == '__mian__':
    # distance_point_point
    p1, p2 = np.array([0, 0]), np.array([1, 1])
    distance = distance_point_point(p1, p2)
    assert distance - 1.4142135623730951 < .000001

    # distance_segment_point
    p = np.array([0, 5])
    segment = [np.array([0, 0]), np.array([10, 10])]
    distance = distance_segment_point(segment, p)
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
    distance = distance_polyline_point(polyline, p)
    assert distance - 3.5355339059327373 < .000001

    # point_at_parameter_segement
    p = point_at_parameter_segement(segment, .5)
    assert p == np.array([5, 5])

    # point_at_parameter_polyline
    p = point_at_parameter_polyline(polyline, .3)
