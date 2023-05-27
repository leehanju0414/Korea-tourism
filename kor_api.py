import requests
import xml.etree.ElementTree as ET

# 공공데이터 API 키 (Decoding)
api_key = "6yz0bWs7lsT7OEp3s2Zb1/+jx7qOFqNT18qCdMYOLc9PhxYdxrJ+Y78g0dPjztos2oMgCvbNDwjtL65zRi4/OQ=="


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
            "lat": item.findtext("mapy"),
            "lng": item.findtext("mapx")
        }
        tour_infoes.append(tour_info)

    # api 잘 읽어오는지 test
    for data in tour_infoes:
            print("Title:", data["title"])
            print("Address:", data["address"])
            print("Latitude:", data["lat"])
            print("Longitude:", data["lng"])
            print("-----")

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

    content_types = []




