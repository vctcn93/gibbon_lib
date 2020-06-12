from ._keys import AMAP_KEY
from gibbon.utility import Convert
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import pandas as pd
import json


class Amap:
    def __init__(self, key=AMAP_KEY):
        self.key = key

    def set_key(self, key: str):
        """
        :param key: 用户在高德地图官网申请的用户唯一标识
        """
        self.key = key

    def division_by_name_subdistrict(
        self,
        keywords: str,
        subdistrict: int = 0,
        page: int = 1,
        offset: int = 20,
        extensions: str = 'all',
        fillter: str = '',
        callback: str = '',
        output: str = 'JSON'
    ) -> pd.DataFrame:
        """
        获取行政区划的详细信息
        :param keywords: 查询关键字
                        规则：只支持单个关键词语搜索关键词支持：行政区名称、citycode、adcode
                        例如，在subdistrict=2，搜索省份（例如山东），能够显示市（例如济南），区（例如历下区）
                        adcode信息可参考城市编码表获取
        :param subdistrict: 子级行政区
                        规则：设置显示下级行政区级数（行政区级别包括：国家、省/直辖市、市、区/县、乡镇/街道多级数据）
                        可选值：0、1、2、3等数字，并以此类推
                        0：不返回下级行政区；
                        1：返回下一级行政区；
                        2：返回下两级行政区；
                        3：返回下三级行政区；
                        需要在此特殊说明，目前部分城市和省直辖县因为没有区县的概念，故在市级下方直接显示街道。
                        例如：广东-东莞、海南-文昌市
        :param page: 需要第几页数据
        :param offset: 最外层返回数据个数
        :param extensions: 返回结果控制
                        此项控制行政区信息中返回行政区边界坐标点； 可选值：base、all;
                        base:不返回行政区边界坐标点；
                        all:只返回当前查询district的边界值，不返回子节点的边界值；
                        目前不能返回乡镇/街道级别的边界值
        :param fillter: 根据区划过滤
        :param callback: 回调函数
        :param output: 返回数据格式类型
        :return:pd.DataFrame
        """

        url = 'https://restapi.amap.com/v3/config/district?'
        params = {
            'key': self.key,
            'keywords': keywords,
            'subdistrict': subdistrict,
            'offset': offset,
            'page': page,
            'extensions': extensions,
            'fillter': fillter,
            'callback': callback,
            'output': output
        }

        response = requests.get(url, params=params)
        content = json.loads(response.content)

        def get_districts(data):
            result = list()

            if len(data['districts']) == 0:
                result += [data]

            else:
                for dt in data['districts']:
                    result += get_districts(dt)
            return result

        data = get_districts(content)
        results = pd.DataFrame(data)
        results['coord_sys'] = 'gcj02'

        return results

    def pois_by_keyword_lnglat_radius(
        self,
        keywords: str,
        lnglat: tuple,
        radius: int,
        types: str = '',
        city: str = '',
        sortrule: str = 'distance',
        offset: int = 20,
        page: int = 1,
        extensions: str = 'all'
    ) -> pd.DataFrame:
        """
        :param lnglat: 中心点坐标。规则： 经度和纬度用","分割，经度在前，纬度在后，经纬度小数点后不得超过6位
        :param keywords: 查询关键字。规则： 多个关键字用“|”分割
        :param types: 查询POI类型
        :param city: 查询城市
        :param radius: 查询半径。取值范围:0-50000。规则：大于50000按默认值，单位：米
        :param sortrule: 排序规则。按距离排序：distance；综合排序：weight
        :param offset: 每页记录数据，强烈建议不超过25，若超过25可能造成访问报错
        :param page: 当前页数
        :param extensions: 此项默认返回基本地址信息；取值为 'all' 返回地址信息、附近POI、道路以及道路交叉口信息。
        :return: pd.DataFrame
        """
        results = list()
        gcj02 = Convert.wgs84togcj02(lnglat)
        str_lnglat = Convert.to_string(gcj02)

        url = 'https://restapi.amap.com/v3/place/around?'
        params = {
            'key': self.key,
            'location': str_lnglat,
            'keywords': keywords,
            'types': types,
            'city': city,
            'radius': radius,
            'sortrule': sortrule,
            'offset': offset,
            'page': page,
            'extensions': extensions
        }

        response = requests.get(url, params=params)
        content = json.loads(response.content)
        results += content['pois']

        turns = int(eval(content['count'])/offset)

        for i in range(1, turns + 1):
            params['page'] = i + 1
            response = requests.get(url, params=params)
            content = json.loads(response.content)
            results += content['pois']

        df = pd.DataFrame(results)
        df['coord_sys'] = 'gcj02'

        return df

    def pois_by_keyword_city(
        self,
        keywords: str,
        city: str,
        types: str = '',
        citylimit: str = 'false',
        children: int = 0,
        page: int = 1,
        offset: int = 20,
        building: str = '',
        floor: str = '',
        extensions: str = 'all'
    ) -> pd.DataFrame:
        """

        :param keywords: 查询关键字。规则： 多个关键字用“|”分割
        :param city: 查询城市
        :param types: 查询POI类型
        :param citylimit: 仅返回指定城市数据。可选值：'true'/'false'
        :param children: 是否按照层级展示子POI数据
        :param page: 当前页数
        :param offset: 每页记录数据，强烈建议不超过25，若超过25可能造成访问报错
        :param building: 建筑物的POI编号
        :param floor: 搜索楼层
        :param extensions: 此项默认返回基本地址信息；取值为 'all' 返回地址信息、附近POI、道路以及道路交叉口信息。
        :return: pd.DataFrame
        """
        results = list()
        url = 'https://restapi.amap.com/v3/place/text?'
        params = {
            'key': self.key,
            'keywords': keywords,
            'city': city,
            'types': types,
            'citylimit': citylimit,
            'children': children ,
            'offset': offset,
            'page': page,
            'building': building,
            'floor': floor,
            'extensions': extensions
        }

        response = requests.get(url, params=params)
        content = json.loads(response.content)
        results += content['pois']

        turns = int(eval(content['count'])/offset)

        for i in range(1, turns + 1):
            params['page'] = i + 1
            response = requests.get(url, params=params)
            content = json.loads(response.content)
            results += content['pois']

        df = pd.DataFrame(results)
        df['coord_sys'] = 'gcj02'

        return df

    def walking_path_by_origin_destination(
        self,
        origin: tuple,
        destination: tuple
    ) -> pd.DataFrame:
        """
        可以规划100KM以内的步行通勤方案，并且返回通勤方案的数据。
        :param origin: 出发点，经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        :param destination: 目的地，经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        :return:list[list[tuple(float)]]
        """
        points = [origin, destination]
        gcj02s = map(Convert.wgs84togcj02, points)
        str_ps = list(map(Convert.to_string, gcj02s))

        url = 'https://restapi.amap.com/v3/direction/walking?'
        params = {
            'key': self.key,
            'origin': str_ps[0],
            'destination': str_ps[1]
        }

        response = requests.get(url, params=params)
        content = json.loads(response.content)

        data = content['route']['paths'][0]['steps']
        results = pd.DataFrame(data)
        results['coord_sys'] = 'gcj02'

        return results

    def driving_path_by_origin_destination(
        self,
        origin: tuple,
        destination: tuple,
        strategy: int = 10,
        waypoints: str = '',
        avoidpolygons: str = '',
        avoidroad: str = '',
        province: str = '',
        number: str = '',
        cartype: int = 0,
        ferry: int = 0,
        roadaggregation: str = 'flase',
        extensions: str = 'all'
    ) -> list:
        """
        获得由高德开发者平台计算出的二点驾车路径
        :param origin: 出发点，经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        :param destination: 目的地，经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        :param strategy: 下方策略 0~9的策略，仅会返回一条路径规划结果。
                0，速度优先，不考虑当时路况，此路线不一定距离最短
                1，费用优先，不走收费路段，且耗时最少的路线
                2，距离优先，不考虑路况，仅走距离最短的路线，但是可能存在穿越小路/小区的情况
                3，速度优先，不走快速路，例如京通快速路（因为策略迭代，建议使用13）
                4，躲避拥堵，但是可能会存在绕路的情况，耗时可能较长
                5，多策略（同时使用速度优先、费用优先、距离优先三个策略计算路径）。

            其中必须说明，就算使用三个策略算路，会根据路况不固定的返回一~三条路径规划信息。
                6，速度优先，不走高速，但是不排除走其余收费路段
                7，费用优先，不走高速且避免所有收费路段
                8，躲避拥堵和收费，可能存在走高速的情况，并且考虑路况不走拥堵路线，但有可能存在绕路和时间较长
                9，躲避拥堵和收费，不走高速

            下方策略返回多条路径规划结果
                10，返回结果会躲避拥堵，路程较短，尽量缩短时间，与高德地图的默认策略也就是不进行任何勾选一致
                11，返回三个结果包含：时间最短；距离最短；躲避拥堵 （由于有更优秀的算法，建议用10代替）
                12，返回的结果考虑路况，尽量躲避拥堵而规划路径，与高德地图的“躲避拥堵”策略一致
                13，返回的结果不走高速，与高德地图“不走高速”策略一致
                14，返回的结果尽可能规划收费较低甚至免费的路径，与高德地图“避免收费”策略一致
                15，返回的结果考虑路况，尽量躲避拥堵而规划路径，并且不走高速，与高德地图的“躲避拥堵&不走高速”策略一致
                16，返回的结果尽量不走高速，并且尽量规划收费较低甚至免费的路径结果，与高德地图的“避免收费&不走高速”策略一致
                17，返回路径规划结果会尽量的躲避拥堵，并且规划收费较低甚至免费的路径结果，与高德地图的“躲避拥堵&避免收费”策略一致
                18，返回的结果尽量躲避拥堵，规划收费较低甚至免费的路径结果，并且尽量不走高速路，与高德地图的“避免拥堵&避免收费&不走高速”策略一致
                19，返回的结果会优先选择高速路，与高德地图的“高速优先”策略一致
                20，返回的结果会优先考虑高速路，并且会考虑路况躲避拥堵，与高德地图的“躲避拥堵&高速优先”策略一致

        :param waypoints: 途经点，经度和纬度用","分割，经度在前，纬度在后，小数点后不超过6位，坐标点之间用";"分隔
        :param avoidpolygons: 避让区域
        :param avoidroad: 避让道路名
        :param province: 用汉字填入车牌省份缩写，用于判断是否限行
        :param number: 车牌的字母和数字（需大写）。用于判断限行相关。
        :param cartype: 车辆类型
                0：普通汽车(默认值)
                1：纯电动车
                2：插电混动车

        :param ferry: 在路径规划中，是否使用轮渡
                0:使用渡轮(默认)
                1:不使用渡轮

        :param roadaggregation: 是否返回路径聚合信息
        :param extensions: 返回结果控制
                base：返回基本信息
                all：返回全部信息
        :return: list[list[tuple(float)]]
        """
        points = [origin, destination]
        gcj02s = map(Convert.wgs84togcj02, points)
        str_ps = list(map(Convert.to_string, gcj02s))

        url = 'https://restapi.amap.com/v3/direction/driving?'
        params = {
            'key': self.key,
            'origin': str_ps[0],
            'destination': str_ps[1],
            'strategy': strategy,
            'waypoints': waypoints,
            'avoidpolygons': avoidpolygons,
            'avoidroad': avoidroad,
            'province': province,
            'number': number,
            'cartype': cartype,
            'ferry': ferry,
            'roadaggregation': roadaggregation,
            'extensions': extensions
        }

        response = requests.get(url, params=params)
        content = json.loads(response.content)

        data = content['route']['paths'][0]['steps']
        results = pd.DataFrame(data)
        results['coord_sys'] = 'gcj02'

        return results

    def transit_path_by_origin_destination_city(
        self,
        origin: tuple,
        destination: tuple,
        city: str,
        cityd: str = '',
        extensions: str = 'all',
        strategy: int = 0,
        nightflag: int = 0
    ):
        """

        :param origin: 出发点，经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        :param destination: 目的地，经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        :param city: 目前支持市内公交换乘/跨城公交的起点城市。
        :param cityd: 跨城公交规划时的终点城市，跨城公交规划必填参数。
        :param extensions: base:返回基本信息；all：返回全部信息
        :param strategy: 公交换乘策略
                0：最快捷模式
                1：最经济模式
                2：最少换乘模式
                3：最少步行模式
                5：不乘地铁模式

        :param nightflag: 是否计算夜班车
                0：不计算夜班车
                1：计算夜班车
        :return: list[dict{}]
        """
        points = [origin, destination]
        gcj02s = map(Convert.wgs84togcj02, points)
        str_ps = list(map(Convert.to_string, gcj02s))

        url = 'https://restapi.amap.com/v3/direction/transit/integrated?'
        params = {
            'key': self.key,
            'origin': str_ps[0],
            'destination': str_ps[1],
            'city': city,
            'cityd': cityd,
            'extensions': extensions,
            'strategy': strategy,
            'nightflag': nightflag
        }

        response = requests.get(url, params=params)
        content = json.loads(response.content)

        transits = content['route']['transits']
        results = pd.DataFrame(transits)
        results['coord_sys'] = 'gcj02'

        return results

    def road_by_keyword_city(
            self,
            keyword: str,
            city: str
    ) -> list:
        """
        通过路名与城市名获取道路信息
        :param keyword: 道路名称
        :param city: 所在城市
        :return: list[Road]
        """
        url = f'http://restapi.amap.com/v3/road/roadname?'
        params = {
            'key': self.key,
            'keywords': keyword,
            'city': city
        }

        response = requests.get(url, params=params)
        content = json.loads(response.content)
        roads = content['roads']

        return pd.DataFrame(roads)

    @staticmethod
    def texture_by_tile_index(
            tile_index,
            style: str = 'normal',
            show: bool = False
    ):
        x, y, z = tile_index

        if style == 'site':
            kind = 6
        elif style == 'normal':
            kind = 7
        elif style == 'dark':
            kind = 8
        else:
            kind = 7

        url = 'http://wprd03.is.autonavi.com/appmaptile?' 
        params = {
            'style': kind,
            'x': x,
            'y': y,
            'z': z
        }

        response = requests.get(url, params=params)
        img = Image.open(BytesIO(response.content))

        if show:
            img.show()

        rgb = img.convert('RGB')
        return np.array(rgb).astype(int)

    @staticmethod
    def metro_by_link(link):
        result = dict()
        response = requests.get(link)
        data = json.loads(response.content)

        main_data = data['data']
        metro_name = data['searchOpt']['keyword']

        bounds = main_data['bounds']
        bounds = bounds.split(';')
        bounds = list(map(Convert.to_tuple, bounds))

        busline_list = main_data['busline_list'][0]
        lngs = list(map(eval, busline_list['xs'].split(',')))
        lats = list(map(eval, busline_list['ys'].split(',')))
        lnglats = list(zip(lngs, lats))
        stations = busline_list['stations']

        station_lnglats = list()
        for station in stations:
            name = station['name']
            lnglat = list(map(Convert.to_tuple, station['xy_coords'].split(';')))
            station_lnglats.append({name: lnglat})

        result['name'] = metro_name
        result['bounds'] = bounds
        result['polyline'] = lnglats
        result['stations'] = station_lnglats

        return result
