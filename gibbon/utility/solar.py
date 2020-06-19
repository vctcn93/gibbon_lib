from pysolar import solar
import datetime
import numpy as np


def angles_by_lnglat_date(lnglat: list, date: list):
    moments = [
        datetime.datetime(
            *date, i, tzinfo=datetime.timezone.utc
        ) for i in range(24)
    ]

    angles = list()

    for mom in moments:
        altitude = solar.get_altitude(lnglat[1], lnglat[0], mom)

        if altitude > 0:
            azimuth = solar.get_azimuth(lnglat[1], lnglat[0], mom)
            angle = [altitude, azimuth]
            angles.append(angle)

    return angles


if __name__ == '__main__':
    origin = [113.520280, 22.130790]
    date = [2020, 12, 25]
    print(angles_by_lnglat_date(origin, date))
