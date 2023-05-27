import requests
import xml.etree.ElementTree as ET

# 공공데이터 API 키 (Decoding)
api_key = ""


def Area_Based(pageNo, ContentTypeId, Areacode, Sigungucode):

    area_Based_url = "http://apis.data.go.kr/B551011/KorService1/areaBasedList1"

    params = {
        "numOfRows": 100,
        "pageNo": pageNo,
        "MobileOS": "ETC",
        "MobileApp": "Korea_tourism",
        "contentTypeId": ContentTypeId,
        "areaCode": Areacode,
        "sigunguCode": Sigungucode,
        "serviceKey": api_key
    }

    response = requests.get(area_Based_url, params=params)
    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    tour_infoes = []
    for item in items:
        tour_info = {
            "title": item.findtext("title"),
            "address": item.findtext("addr1"),
            "firstimage": item.findtext("firstimage"),
            "firstimage2": item.findtext("firstimage2"),
            "lat": item.findtext("mapy"),
            "lng": item.findtext("mapx")
        }
        tour_infoes.append(tour_info)

    return tour_infoes


def Area_Code():

    area_code_url = "http://apis.data.go.kr/B551011/KorService1/areaCode1"
    params = {
        "numOfRows": 50,
        "MobileOS": "ETC",
        "MobileApp": "Korea_tourism",
        "serviceKey": api_key
    }

    response = requests.get(area_code_url, params=params)
    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    area_codes = []

    for item in items:
        area_code = {
            "name": item.findtext("name"),
            "code": item.findtext("code")
        }
        area_codes.append(area_code)

    return area_codes


def Sigungu_Code(area_code):

    area_code_url = "http://apis.data.go.kr/B551011/KorService1/areaCode1"

    params = {
        "numOfRows": 50,
        "MobileOS": "ETC",
        "MobileApp": "Korea_tourism",
        "areaCode": area_code,
        "serviceKey": api_key
    }

    response = requests.get(area_code_url, params=params)
    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    sigungu_codes = []

    for item in items:
        sigungu_code = {
            "name": item.findtext("name"),
            "code": item.findtext("code")
        }
        sigungu_codes.append(sigungu_code)

    return sigungu_codes


def Content_Type():

    content_types = [{'name': '관광지', 'code': '12'}, {'name': '문화시설', 'code': '14'}, {'name': '축제공연행사', 'code': '15'},
                     {'name': '여행코스', 'code': '25'}, {'name': '레포츠', 'code': '28'}, {'name': '숙박', 'code': '32'},
                     {'name': '쇼핑', 'code': '38'}, {'name': '음식점', 'code': '39'}, {'name': '전체', 'code': ''}]

    return content_types