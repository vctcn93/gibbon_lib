from ._keys import BMAP_KEY
from gibbon.utility import Convert
from PIL import Image
from io import BytesIO
import numpy as np
import pandas as pd
import requests
import json


class Bmap:
    def __init__(self, key=BMAP_KEY):
        self.key = key

    def set_key(self, key):
        """
        :param key: 百度开发者的访问密钥
        :return: None
        """
        self.key = key

    def pois_by_keyword_city(
        self,
        keywords: str,
        city: str,
        types: str = '',
        city_limit: str = 'false',
        page: int = 0,
        offset: int = 20,
        extension: int = 2,
        ret_coordtype: str = 'wgs84ll',
        coord_type: int = 1
    ) -> list:
        """
        检索某一行政区划内（目前最细到城市级别）的地点信息
        :param keywords: 检索关键字。行政区划区域检索不支持多关键字检索。
        :param city: 检索行政区划区域（增加区域内数据召回权重，如需严格限制召回数据在区域内，请搭配使用city_limit参数）
        :param types: 检索分类偏好，与q组合进行检索，多个分类以","分隔
        :param city_limit: 区域数据召回限制，为true时，仅召回region对应区域内数据。
        :param page: 分页页码，默认为0,0代表第一页，1代表第二页，以此类推。
        :param offset: 单次召回POI数量，默认为10条记录，最大返回20条。
        :param extension: 检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
        :param ret_coordtype: 可选参数，添加后POI返回wgs84经纬度坐标
        :param coord_type: 坐标类型。
                1（wgs84ll即GPS经纬度）
                2（gcj02ll即国测局经纬度坐标）
                3（bd09ll即百度经纬度坐标）
                4（bd09mc即百度米制坐标）
        :return: list[Poi]
        """
        pois = list()

        url = 'http://api.map.baidu.com/place/v2/search?'
        params = {
            'ak': self.key,
            'query': keywords,
            'region': city,
            'tag': types,
            'city_limit': city_limit,
            'page_num': page,
            'page_size': offset,
            'ret_coordtype': ret_coordtype,
            'coord_type': coord_type,
            'scope': extension,
            'output': 'json'
        }
        response = requests.get(url, params)
        content = json.loads(response.content)
        pois += content['results']
        quantity = content['total']
        turns =  int(quantity / offset)

        for i in range(1, turns+1):
            params['page_num'] = i
            response = requests.get(url, params)
            content = json.loads(response.content)
            pois += content['results']

        return pd.DataFrame(pois)

    def pois_by_lnglat_radius_keyword(
        self,
        lnglat: tuple,
        radius: int,
        keywords: str,
        radius_limit: str = 'true',
        types: str = '',
        page: int = 0,
        offset: int = 20,
        extension: int = 2,
        ret_coordtype: str = 'wgs84ll',
        coord_type: int = 1

    ) -> list:
        """
        设置圆心和半径，检索圆形区域内的地点信息
        :param lnglat: 圆形区域检索中心点，不支持多个点
        :param radius: 圆形区域检索半径，单位为米。(当半径过大，超过中心点所在城市边界时，会变为城市范围检索，检索范围为中心点所在城市）
        :param keywords: 检索关键字。圆形区域检索和矩形区域内检索支持多个关键字并集检索，不同关键字间以$符号分隔，最多支持10个关键字检索。
        :param radius_limit: 是否严格限定召回结果在设置检索半径范围内。
        :param types: 检索分类偏好，与q组合进行检索，多个分类以","分隔
        :param page: 分页页码，默认为0,0代表第一页，1代表第二页，以此类推。
        :param offset: 单次召回POI数量，默认为10条记录，最大返回20条。
        :param extension:  检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
        :param ret_coordtype: 可选参数，添加后POI返回wgs84经纬度坐标
        :param coord_type: 坐标类型。
                1（wgs84ll即GPS经纬度）
                2（gcj02ll即国测局经纬度坐标）
                3（bd09ll即百度经纬度坐标）
                4（bd09mc即百度米制坐标）
        :return: pd.DataFrame
        """
        pois = list()
        lnglat.reverse()
        lnglat = Convert.to_string(lnglat)

        url = 'http://api.map.baidu.com/place/v2/search?'
        params = {
            'ak': self.key,
            'query': keywords,
            'location': lnglat,
            'radius': radius,
            'tag': types,
            'radius_limit': radius_limit,
            'page_num': page,
            'page_size': offset,
            'ret_coordtype': ret_coordtype,
            'coord_type': coord_type,
            'scope': extension,
            'output': 'json'
        }

        response = requests.get(url, params)
        content = json.loads(response.content)
        pois += content['results']
        quantity = content['total']
        turns =  int(quantity / offset)

        for i in range(1, turns+1):
            params['page_num'] = i
            response = requests.get(url, params)
            content = json.loads(response.content)
            pois += content['results']

        return pd.DataFrame(pois)

    def pois_by_keyword_bounds(
        self,
        keywords: str,
        bounds: list,  # [116.404,39.915,116.414,39.975]
        types: str = '',
        page: int = 0,
        offset: int = 20,
        extension: int = 2,
        ret_coordtype: str = 'wgs84ll',
        coord_type: int = 1
    ) -> list:
        """
        设置检索区域左下角和右上角坐标，检索坐标对应矩形内的地点信息
        :param keywords: 检索关键字。行政区划区域检索不支持多关键字检索。
        :param bounds: 检索矩形区域，多组坐标间以","分隔
        :param types: 检索分类偏好，与q组合进行检索，多个分类以","分隔
        :param page: 分页页码，默认为0,0代表第一页，1代表第二页，以此类推。
        :param offset: 单次召回POI数量，默认为10条记录，最大返回20条。
        :param extension: 检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
        :param ret_coordtype: 可选参数，添加后POI返回国测局经纬度坐标
        :param coord_type: 坐标类型。
                1（wgs84ll即GPS经纬度）
                2（gcj02ll即国测局经纬度坐标）
                3（bd09ll即百度经纬度坐标）
                4（bd09mc即百度米制坐标）
        :return: pd.DataFrame
        """
        pois = list()
        lng_min, lat_min, lng_max, lat_max = bounds
        bounds = f"{Convert.to_string(lat_min)},{Convert.to_string(lng_min)}," \
                + f"{Convert.to_string(lat_max)},{Convert.to_string(lng_max)}"

        url = 'http://api.map.baidu.com/place/v2/search?'
        params = {
            'ak': self.key,
            'query': keywords,
            'bounds': bounds,
            'tag': types,
            'page_num': page,
            'page_size': offset,
            'ret_coordtype': ret_coordtype,
            'coord_type': coord_type,
            'scope': extension,
            'output': 'json'
        }

        response = requests.get(url, params)
        content = json.loads(response.content)
        pois += content['results']
        quantity = content['total']
        turns =  int(quantity / offset)

        for i in range(1, turns+1):
            params['page_num'] = i
            response = requests.get(url, params)
            content = json.loads(response.content)
            pois += content['results']

        return pd.DataFrame(pois)

    def driving_path_by_origin_destination(
        self,
        origin: tuple,
        destination: tuple,
        waypoints: str = '',
        tactics: int = 0,
        coord_type: str = 'wgs84',
        ret_coordtype: str = 'gcj02'
    ) -> list:
        """
        根据起终点坐标规划驾车出行路线和耗时
        :param origin: 起点
        :param destination: 终点
        :param waypoints: 途经点。支持5个以内的有序途径点。多个途径点坐标按顺序以英文竖线符号分隔
        :param tactics: 路线偏好。
                0：常规路线，即多数用户常走的一条经验路线，满足大多数场景需求，是较推荐的一个策略
                1：不走高速
                2：躲避拥堵
        :param coord_type: 输入坐标类型
                bd09ll：百度经纬度坐标
                bd09mc：百度墨卡托坐标
                gcj02：国测局加密坐标
                wgs84：gps设备获取的坐标
        :param ret_coordtype: 输出坐标类型
                bd09ll：百度经纬度坐标
                gcj02：国测局加密坐标
        :return: pd.DataFrame
        """
        s_e = list()
        for item in [origin.copy(), destination.copy()]:
            item.reverse()
            s_e.append(Convert.to_string(item))

        url = 'http://api.map.baidu.com/directionlite/v1/driving?'
        params = {
            'ak': self.key,
            'origin': s_e[0],
            'destination': s_e[1],
            'waypoints': waypoints,
            'tactics': tactics,
            'coord_type': coord_type,
            'ret_coordtype': ret_coordtype
        }

        response = requests.get(url, params)
        content = json.loads(response.content)

        routes = content['result']['routes']
        results = list()

        for route in routes:
            results += route['steps']

        return pd.DataFrame(results)

    def walking_path_by_origin_destination(
        self,
        origin: tuple,
        destination: tuple,
        coord_type: str = 'wgs84',
        ret_coordtype: str = 'gcj02'
    ) -> list:
        """
        根据起终点坐标规划步行出行路线和耗时
        :param origin: 起点
        :param destination: 终点
        :param coord_type: 输入坐标类型
                bd09ll：百度经纬度坐标
                bd09mc：百度墨卡托坐标
                gcj02：国测局加密坐标
                wgs84：gps设备获取的坐标
        :param ret_coordtype: 输出坐标类型
                bd09ll：百度经纬度坐标
                gcj02：国测局加密坐标
        :return: pd.DataFrame
        """
        s_e = list()
        for item in [origin.copy(), destination.copy()]:
            item.reverse()
            s_e.append(Convert.to_string(item))

        url = 'http://api.map.baidu.com/directionlite/v1/walking?'
        params = {
            'ak': self.key,
            'origin': s_e[0],
            'destination': s_e[1],
            'coord_type': coord_type,
            'ret_coordtype': ret_coordtype
        }

        response = requests.get(url, params)
        content = json.loads(response.content)

        routes = content['result']['routes']
        results = list()

        for route in routes:
            results += route['steps']

        return pd.DataFrame(results)

    def transit_path_by_origin_destination(
        self,
        origin: tuple,
        destination: tuple,
        coord_type: str = 'wgs84',
        ret_coordtype: str = 'gcj02'
    ) -> list:
        """
        根据起终点坐标规划同城公共交通出行路线和耗时，支持公交、地铁出行方式
        :param origin: 起点
        :param destination: 终点
        :param coord_type: 输入坐标类型
                bd09ll：百度经纬度坐标
                bd09mc：百度墨卡托坐标
                gcj02：国测局加密坐标
                wgs84：gps设备获取的坐标
        :param ret_coordtype: 输出坐标类型
                bd09ll：百度经纬度坐标
                gcj02：国测局加密坐标
        :return: pd.DataFrame
        """
        s_e = list()
        for item in [origin.copy(), destination.copy()]:
            item.reverse()
            s_e.append(Convert.to_string(item))

        url = 'http://api.map.baidu.com/directionlite/v1/transit?'
        params = {
            'ak': self.key,
            'origin': s_e[0],
            'destination': s_e[1],
            'coord_type': coord_type,
            'ret_coordtype': ret_coordtype
        }
        response = requests.get(url, params)
        content = json.loads(response.content)

        routes = content['result']['routes']
        results = list()

        for route in routes:
            results += route['steps']

        return pd.DataFrame(results)

    def lnglat_by_address_city(
        self,
        address: str,
        city: str,
        ret_coordtype: str = 'gcj02ll'
    ) -> list:
        """
        正地理编码服务提供将结构化地址数据（如：北京市海淀区上地十街十号）转换为对应坐标点（经纬度）功能
        如果无搜索结果，将返回空值
        :param address: 待解析的地址。最多支持84个字节。
        :param city: 地址所在的城市名。
        :param ret_coordtype: 输出坐标类型
        :return: list
        """
        url = 'http://api.map.baidu.com/geocoder/v2/?'
        params = {
            'ak': self.key,
            'address': address,
            'city': city,
            'ret_coordtype': ret_coordtype,
            'output': 'json',
            'allback': 'showLocation'

        }

        response = requests.get(url, params)
        content = json.loads(response.content)
        result = content['result']
        return [result['location']['lng'], result['location']['lat']]

    def static_image(
        self,
        lnglat: tuple,
        width: int = '',
        height: int = '',
        scale: int = '',
        bbox: str = '',
        zoom: float = '',
        coordtype: str = 'wgs84ll',
        show: bool = False
    ):
        """
        返回百度申请的静态地图
        :param lnglat: 地图中心点位置，参数可以为经纬度坐标或名称。坐标格式：lng<经度>，lat<纬度>，[116.43213,38.76623]。
        :param width: 图片宽度。取值范围：(0, 1024]。Scale=2,取值范围：(0, 512]。
        :param height: 图片高度。取值范围：(0, 1024]。Scale=2,取值范围：(0, 512]。
        :param scale: 返回图片大小会根据此标志调整。取值范围为1或2：
                    1表示返回的图片大小为size= width * height;
                    2表示返回图片为(width*2)*(height *2)，且zoom加1
                    注：如果zoom为最大级别，则返回图片为（width*2）*（height*2），zoom不变。
        :param bbox: 地图视野范围。格式：minX,minY;maxX,maxY。
        :param zoom: 地图级别。高清图范围[3, 18]；低清图范围[3,19]
        :param coordtype: 静态图的坐标类型。
                    支持wgs84ll（wgs84坐标）/gcj02ll（国测局坐标）/bd09ll（百度经纬度）/bd09mc（百度墨卡托）。默认bd09ll（百度经纬度）
        :param show: 是否临时显示图片
        :return: 区域的静态地图图片
        """
        # 官方API，经前纬后
        lnglat = Convert.to_string(lnglat)

        url = 'http://api.map.baidu.com/staticimage/v2?'
        params = {
            'ak': self.key,
            'center': lnglat,
            'width': width,
            'height': height,
            'scale': scale,
            'bbox': bbox,
            'zoom': zoom,
            'coordtype': coordtype
        }

        response = requests.get(url, params=params)
        img = Image.open(BytesIO(response.content))

        if show:
            img.show()

        rgb = img.convert('RGB')
        return np.array(rgb).astype(int)

    def reverse_geocoding(
        self,
        lnglat: tuple,
        coordtype: str = 'wgs84ll',
        ret_coordtype: str = 'gcj02ll',
        radius: int = 1000,
        sn: str = '',
        output='json',
        callback='',
        extensions_poi: int = 0,
        extensions_road: str = 'flase',
        extensions_town: str = 'true',
        language: str = 'zh-CN',
        language_auto: int = 1
    ) -> str:
        """
        :param lnglat: 根据经纬度坐标获取地址。
        :param coordtype: 发送的坐标的类型
        :param ret_coordtype: 后返回国测局经纬度坐标或百度米
        :param radius: poi召回半径，允许设置区间为0-1000米，超过1000米按1000米召回
        :param sn: 若用户所用ak的校验方式为sn校验时该参数必须
        :param output: 输出格式为json或者xml
        :param callback: 将json格式的返回值通过callback函数返回以实现jsonp功能
        :param extensions_poi: extensions_poi=0，不召回pois数据
                                extensions_poi=1，返回pois数据，默认显示周边1000米内的poi。
        :param extensions_road: 当取值为true时，召回坐标周围最近的3条道路数据。
                                区别于行政区划中的street参数（street参数为行政区划中的街道，和普通道路不对应）。
        :param extensions_town: 当取值为true时，行政区划返回乡镇级数据（仅国内召回乡镇数据）。默认不访问。
        :param language: 指定召回的新政区划语言类型。
        :param language_auto: 是否自动填充行政区划，1填充，0不填充。
        :return:
        """
        lnglat = Convert.to_string(lnglat.copy().reverse())

        url = 'http://api.map.baidu.com/reverse_geocoding/v3/?'
        params = {
            'ak': self.key,
            'location': lnglat,
            'coordtype': coordtype,
            'ret_coordtype': ret_coordtype,
            'radius': radius,
            'sn': sn,
            'output': output,
            'callback': callback,
            'extensions_poi': extensions_poi,
            'extensions_road': extensions_road,
            'extensions_town': extensions_town,
            'language': language,
            'language_auto': language_auto
        }

        response = requests.get(url, params)
        content = json.loads(response.content)
        return content['result']['formatted_address']
