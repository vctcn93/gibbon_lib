import math
from .constance import *


def _is_in_china(func):
    def wrapper(lnglat):
        if 72.004 < lnglat[0] < 137.8347 and .8293 < lnglat[1] < 55.8271:
            return func(lnglat)
        return lnglat
    return wrapper


def _transform_lng(lng: float, lat: float) -> float:
        ret = 300 + lng + 2 * lat + .1 * lng * lng + \
              .1 * lng * lat + .1 * math.sqrt(math.fabs(lng))
        ret += (20 * math.sin(6.0 * lng * PI) + 20 *
                math.sin(2 * lng * PI)) * 2 / 3
        ret += (20 * math.sin(lng * PI) + 40 *
                math.sin(lng / 3 * PI)) * 2 / 3
        ret += (150 * math.sin(lng / 12 * PI) + 300 *
                math.sin(lng / 30 * PI)) * 2 / 3
        return ret


def _transform_lat(lng: float, lat: float) -> float:
        ret = -100 + 2 * lng + 3 * lat + .2 * lat * lat + \
              .1 * lng * lat + .2 * math.sqrt(math.fabs(lng))
        ret += (20 * math.sin(6.0 * lng * PI) + 20 *
                math.sin(2 * lng * PI)) * 2 / 3
        ret += (20 * math.sin(lat * PI) + 40 *
                math.sin(lat / 3 * PI)) * 2 / 3
        ret += (160 * math.sin(lat / 12 * PI) + 320 *
                math.sin(lat * PI / 30)) * 2 / 3
        return ret


@_is_in_china
def wgs84togcj02(lnglat: list) -> list:
    """
    将wgs84坐标系转为火星坐标
    :param lnglat: list[float] 经纬度数组
    :return: list[float] 经纬度数组
    """
    dlng = _transform_lng(lnglat[0] - 105, lnglat[1] - 35)
    dlat = _transform_lat(lnglat[0] - 105, lnglat[1] - 35)
    radlat = lnglat[1] / 180 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)

    dlat = (dlat * 180) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180) / (A / sqrtmagic * math.cos(radlat) * PI)
    mglat = lnglat[1] + dlat
    mglng = lnglat[0] + dlng

    return [mglng, mglat]


@_is_in_china
def wgs84tobd09(lnglat: list) -> list:
    """
    将wgs84坐标系转为百度坐标
    :param lnglat: list[float] 经纬度数组
    :return: list[float] 经纬度数组
    """
    lnglat = wgs84togcj02(lnglat)
    return gcj02tobd09(lnglat)


@_is_in_china
def gcj02towgs84(lnglat: list) -> list:
    """
    将火星坐标系转为wgs84坐标
    :param lnglat: list[float] 经纬度数组
    :return: list[float] 经纬度数组
    """
    dlat = _transform_lat(lnglat[0] - 105, lnglat[1] - 35)
    dlng = _transform_lng(lnglat[0] - 105, lnglat[1] - 35)
    radlat = lnglat[1] / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)

    dlat = (dlat * 180) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180) / (A / sqrtmagic * math.cos(radlat) * PI)
    mglat = lnglat[1] + dlat
    mglng = lnglat[0] + dlng

    return [lnglat[1] * 2 - mglng, lnglat[0] * 2 - mglat]


@_is_in_china
def gcj02tobd09(lnglat: list) -> list:
    """
    将火星坐标系转为百度坐标
    :param lnglat: list[float] 经纬度数组
    :return: list[float] 经纬度数组
    """
    z = math.sqrt(lnglat[0] * lnglat[0] + lnglat[1] * lnglat[1]) + .00002 * math.sin(lnglat[1] * XPI)
    theta = math.atan2(lnglat[1], lnglat[0]) + .000003 * math.cos(lnglat[0] * XPI)
    bd_lng = z * math.cos(theta) + .0065
    bd_lat = z * math.sin(theta) + .006
    return [bd_lng, bd_lat]


@_is_in_china
def bd09towgs84(lnglat: list) -> list:
    """
    将百度坐标系转为wgs84坐标
    :param lnglat: list[float] 经纬度数组
    :return: list[float] 经纬度数组
    """
    lnglat = bd09togcj02(lnglat)
    return gcj02towgs84(lnglat)


def bd09togcj02(lnglat: list) -> list:
    """
    将百度坐标系转为火星坐标
    :param lnglat: list[float] 经纬度数组
    :return: list[float] 经纬度数组
    """
    x = lnglat[0] - .0065
    y = lnglat[1] - .006
    z = math.sqrt(x * x + y * y) - .00002 * math.sin(y * XPI)
    theta = math.atan2(y, x) - .000003 * math.cos(x * XPI)
    gcj_lng = z * math.cos(theta)
    gcj_lat = z * math.sin(theta)
    return [gcj_lng, gcj_lat]


def lnglat_to_mercator(
        lnglat: list,
        reference_position=(0, 0),
        convert_rate=(1, 1),
        unit='mm'
) -> list:
    """
    将经纬度坐标二维展开为平面坐标
    :param lnglat: list[float] 经纬度
    :param reference_position: list 经纬度参照零点坐标，如城市中心或项目中心
    :param convert_rate: list 形变比例
    :return: list 展开后的二纬坐标
    """
    x = lnglat[0] - reference_position[0]
    y = lnglat[1] - reference_position[1]

    x = x * MERCATOR
    y = math.log(math.tan((90 + y) * PI / 360)) / (PI / 180)
    y = y * MERCATOR

    if unit == 'mm':
        x *= 1000
        y *= 1000

    return [x * convert_rate[0], y * convert_rate[1]]


def mercator_to_lnglat(
        mercator,
        reference_position=(0, 0),
        convert_rate=(1, 1)
) -> list:
    """
    将平面座标回经纬度坐标
    :param mercator: list[float] 墨卡托 xy 坐标
    :param reference_position: list 经纬度参照零点坐标，如城市中心或项目中心
    :param convert_rate: list 形变比例
    :return: list 回归后的经纬度
    """
    x, y = mercator[0] / convert_rate[0], mercator[1] / convert_rate[1]
    x, y = x / MERCATOR, y / MERCATOR
    y = 180 / PI * (2 * math.atan(math.exp(y * PI / 180)) - PI / 2)
    x += reference_position[0]
    y += reference_position[1]

    return [x, y]


def lnglat_to_tile_index(lnglat: list, level: int) -> list:
    n = 2 ** level
    x = int((lnglat[0] + 180.0) / 360.0 * n)
    lat_rad = math.radians(lnglat[1])
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / PI) / 2.0 * n)
    return [x, y, level]


def tile_index_to_lnglat(tiles) -> list:
    n = 2 ** tiles[2]
    lng = tiles[0] / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tiles[1] / n)))
    lat = math.degrees(lat_rad)
    return [lng, lat]


def indices_by_lnglat_level_radius(lnglat: list, level: int, radius: float) -> list:
    result = list()

    x, y, z = lnglat_to_tile_index(lnglat, level)
    tile_size = tile_size_by_zoom(z, 'm')
    num = int(radius / tile_size)

    xstart, ystart = x - num, y - num

    for i in range(int(2 * num)):
        for j in range(int(2 * num)):
            result.append([int(xstart + i), int(ystart + j), z])

    return result


def tile_size_by_zoom(level: int, unit='mm'):
    """
    得到某等级下每片瓦片的标准大小
    :param level:
    :return:
    """
    a =  SIZE * 2 ** (- level - 1)
    return a * 1000 if unit == 'mm' else a


def rgb_to_hex(rgb: tuple) -> str:
    return '#%02x%02x%02x' % tuple(rgb)


def hex_to_rgb(hex: str) -> tuple:
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
