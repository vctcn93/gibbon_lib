import math
import numpy as np


def _is_in_china(func):
    def wrapper(cls, lnglat):
        if 72.004 < lnglat[0] < 137.8347 and .8293 < lnglat[1] < 55.8271:
            return func(cls, lnglat)
        return lnglat
    return wrapper


class Convert:
    _XPI = math.pi * 3000 / 180
    _PI = math.pi
    _A = 6378245
    _EE = .00669342162296594323
    _MERCATOR = 20037508.34 / 180
    _SIZE = 78271516

    @classmethod
    def _transform_lng(cls, lng: float, lat: float) -> float:
            ret = 300 + lng + 2 * lat + .1 * lng * lng + \
                .1 * lng * lat + .1 * math.sqrt(math.fabs(lng))
            ret += (20 * math.sin(6.0 * lng * cls._PI) + 20 *
                    math.sin(2 * lng * cls._PI)) * 2 / 3
            ret += (20 * math.sin(lng * cls._PI) + 40 *
                    math.sin(lng / 3 * cls._PI)) * 2 / 3
            ret += (150 * math.sin(lng / 12 * cls._PI) + 300 *
                    math.sin(lng / 30 * cls._PI)) * 2 / 3
            return ret

    @classmethod
    def _transform_lat(cls, lng: float, lat: float) -> float:
            ret = -100 + 2 * lng + 3 * lat + .2 * lat * lat + \
                .1 * lng * lat + .2 * math.sqrt(math.fabs(lng))
            ret += (20 * math.sin(6.0 * lng * cls._PI) + 20 *
                    math.sin(2 * lng * cls._PI)) * 2 / 3
            ret += (20 * math.sin(lat * cls._PI) + 40 *
                    math.sin(lat / 3 * cls._PI)) * 2 / 3
            ret += (160 * math.sin(lat / 12 * cls._PI) + 320 *
                    math.sin(lat * cls._PI / 30)) * 2 / 3
            return ret

    @classmethod
    @_is_in_china
    def wgs84togcj02(cls, lnglat: list) -> list:
        """
        将wgs84坐标系转为火星坐标
        :param lnglat: list[float] 经纬度数组
        :return: list[float] 经纬度数组
        """
        dlng = cls._transform_lng(lnglat[0] - 105, lnglat[1] - 35)
        dlat = cls._transform_lat(lnglat[0] - 105, lnglat[1] - 35)
        radlat = lnglat[1] / 180 * cls._PI
        magic = math.sin(radlat)
        magic = 1 - cls._EE * magic * magic
        sqrtmagic = math.sqrt(magic)

        dlat = (dlat * 180) / ((cls._A * (1 - cls._EE)) / (magic * sqrtmagic) * cls._PI)
        dlng = (dlng * 180) / (cls._A / sqrtmagic * math.cos(radlat) * cls._PI)
        mglat = lnglat[1] + dlat
        mglng = lnglat[0] + dlng

        return [mglng, mglat]


    @classmethod
    @_is_in_china
    def wgs84tobd09(cls, lnglat: list) -> list:
        """
        将wgs84坐标系转为百度坐标
        :param lnglat: list[float] 经纬度数组
        :return: list[float] 经纬度数组
        """
        lnglat = cls.wgs84togcj02(lnglat)
        return cls.gcj02tobd09(lnglat)

    @classmethod
    @_is_in_china
    def gcj02towgs84(cls, lnglat: list) -> list:
        """
        将火星坐标系转为wgs84坐标
        :param lnglat: list[float] 经纬度数组
        :return: list[float] 经纬度数组
        """
        dlat = cls._transform_lat(lnglat[0] - 105, lnglat[1] - 35)
        dlng = cls._transform_lng(lnglat[0] - 105, lnglat[1] - 35)
        radlat = lnglat[1] / 180.0 * cls._PI
        magic = math.sin(radlat)
        magic = 1 - cls._EE * magic * magic
        sqrtmagic = math.sqrt(magic)

        dlat = (dlat * 180) / ((cls._A * (1 - cls._EE)) / (magic * sqrtmagic) * cls._PI)
        dlng = (dlng * 180) / (cls._A / sqrtmagic * math.cos(radlat) * cls._PI)
        mglat = lnglat[1] + dlat
        mglng = lnglat[0] + dlng

        return [lnglat[0] * 2 - mglng, lnglat[1] * 2 - mglat]

    @classmethod
    @_is_in_china
    def gcj02tobd09(cls, lnglat: list) -> list:
        """
        将火星坐标系转为百度坐标
        :param lnglat: list[float] 经纬度数组
        :return: list[float] 经纬度数组
        """
        z = math.sqrt(lnglat[0] * lnglat[0] + lnglat[1] * lnglat[1]) + .00002 * math.sin(lnglat[1] * cls._XPI)
        theta = math.atan2(lnglat[1], lnglat[0]) + .000003 * math.cos(lnglat[0] * cls._XPI)
        bd_lng = z * math.cos(theta) + .0065
        bd_lat = z * math.sin(theta) + .006
        return [bd_lng, bd_lat]

    @classmethod
    @_is_in_china
    def bd09towgs84(cls, lnglat: list) -> list:
        """
        将百度坐标系转为wgs84坐标
        :param lnglat: list[float] 经纬度数组
        :return: list[float] 经纬度数组
        """
        lnglat = cls.bd09togcj02(lnglat)
        return cls.gcj02towgs84(lnglat)

    @classmethod
    def bd09togcj02(cls, lnglat: list) -> list:
        """
        将百度坐标系转为火星坐标
        :param lnglat: list[float] 经纬度数组
        :return: list[float] 经纬度数组
        """
        x = lnglat[0] - .0065
        y = lnglat[1] - .006
        z = math.sqrt(x * x + y * y) - .00002 * math.sin(y * cls._XPI)
        theta = math.atan2(y, x) - .000003 * math.cos(x * cls._XPI)
        gcj_lng = z * math.cos(theta)
        gcj_lat = z * math.sin(theta)
        return [gcj_lng, gcj_lat]

    @classmethod
    def lnglat_to_mercator(
        cls, 
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

        x = x * cls._MERCATOR
        y = math.log(math.tan((90 + y) * cls._PI / 360)) / (cls._PI / 180)
        y = y * cls._MERCATOR

        if unit == 'mm':
            x *= 1000
            y *= 1000

        return [x * convert_rate[0], y * convert_rate[1]]

    @classmethod
    def mercator_to_lnglat(
        cls, 
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
        x, y = x / cls._MERCATOR, y / cls._MERCATOR
        y = 180 / cls._PI * (2 * math.atan(math.exp(y * cls._PI / 180)) - cls._PI / 2)
        x += reference_position[0]
        y += reference_position[1]

        return [x, y]

    @classmethod
    def lnglat_to_tile_index(cls, lnglat: list, level: int) -> list:
        n = 2 ** level
        x = int((lnglat[0] + 180.0) / 360.0 * n)
        lat_rad = math.radians(lnglat[1])
        y = int((1.0 - math.asinh(math.tan(lat_rad)) / cls._PI) / 2.0 * n)
        return [x, y, level]

    @staticmethod
    def tile_index_to_lnglat(tiles) -> list:
        n = 2 ** tiles[2]
        lng = tiles[0] / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tiles[1] / n)))
        lat = math.degrees(lat_rad)
        return [lng, lat]

    @classmethod
    def tile_size_by_zoom(cls, level: int, unit='mm'):
        """
        得到某等级下每片瓦片的标准大小
        :param level:
        :return:
        """
        a =  cls._SIZE * 2 ** (- level - 1)
        return a * 1000 if unit == 'mm' else a

    @staticmethod
    def rgb_to_hex(rgb: tuple) -> str:
        return '#%02x%02x%02x' % tuple(rgb)

    @staticmethod
    def hex_to_rgb(hex: str) -> tuple:
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def to_list(location: str) -> tuple:
        """
        将字符格式的经纬坐标转为数字列表格式的经纬坐标，用以计算
        :param location: str 如'123.456, 123.456'
        :return: tuple 如(123.456, 123.456)
        """
        # 预设location为'123.456, 123.456'
        return list(eval(location))

    @staticmethod
    def to_string(location: tuple) -> str:
        """
        将数字列表格式的经纬坐标转为字符格式的经纬坐标，用以请求
        :param location: list 如[123.456, 123.456]
        :return: str 如'123.456, 123.456'
        """
        # 预设location为[123.456, 123.456]
        # 输出 '123.456, 123.456'
        return ','.join(list(map(str, location)))

    @staticmethod
    def stringtolist(string, reverse=False):
        """
        string = "113.52546031343,22.129509715856;113.52673029534,22.12949968767;113.52803031317,22.129279677622;113.52832026393,22.129219617399;113.52899033426,22.12907959059;
        113.53028032877,22.128819536949;113.53039032742,22.128789572229;113.5322202692,22.12864953033;113.53390023979,22.128729548104;113.53566024254,22.128759520287;113.5
        3599023855,22.128759507971;113.53607024919,22.128759566279;113.53644027672,22.128759511018;113.53818016921,22.128749559991;113.53828022438,22.128749595569;113.5385
        101591,22.12874961982;113.53944022455,22.128739604046"
        """
        ls = string.split(';')
        c = list(map(eval, ls))
        d = np.array(c)

        if reverse:
            d = np.flip(d, axis=1)

        return d.tolist()
