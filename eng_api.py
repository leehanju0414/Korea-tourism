import requests
import xml.etree.ElementTree as ET

# 공공데이터 API 키 (Decoding)
api_key = ""


def Area_Based(pageNo, ContentTypeId, Areacode, Sigungucode):

    area_Based_url = "http://apis.data.go.kr/B551011/EngService1/areaBasedList1"

    params = {
        "numOfRows": 10000,
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
            "contentid": item.findtext("contentid"),
            "title": item.findtext("title"),
            "address": item.findtext("addr1"),
            "firstimage": item.findtext("firstimage"),
            "contenttypeid": item.findtext("contenttypeid"),
            "lat": item.findtext("mapy"),
            "lng": item.findtext("mapx")
        }
        tour_infoes.append(tour_info)

    # api 잘 읽어오는지 test
    # for data in tour_infoes:
    #         print("Title:", data["title"])
    #         print("ContentID:", data["contentid"])
    #         print("contenttypeid", data['contenttypeid'])
    #         print("Address:", data["address"])
    #         print("Latitude:", data["lat"])
    #         print("Longitude:", data["lng"])
    #         print("-----")

    return tour_infoes

def Detail_Search(contentid):

    detail_search_url = "http://apis.data.go.kr/B551011/EngService1/detailCommon1"

    params = {
        "numOfRows": 100,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "Korea_tourism",
        "contentId": contentid,
        "defaultYN": "Y",
        "overviewYN": "Y",
        "serviceKey": api_key
    }

    response = requests.get(detail_search_url, params=params)
    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    detail_infoes = []
    for item in items:
        detail_info = {
            "title": item.findtext("title"),
            "tel": item.findtext("tel"),
            "homepage": item.findtext("homepage"),
            "overview": item.findtext("overview")
        }
        detail_infoes.append(detail_info)

    # api 잘 읽어오는지 test
    # for data in detail_infoes:
    #         print("Title:", data["title"])
    #         print("tel:", data["tel"])
    #         print("homepage:", data["homepage"])
    #         print("overview:", data["overview"])
    #         print("-----")

    return detail_infoes

def Area_Code():

    area_code_url = "http://apis.data.go.kr/B551011/EngService1/areaCode1"
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

    area_code_url = "http://apis.data.go.kr/B551011/EngService1/areaCode1"

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
    content_types = [{'name': 'Tourist Attractions', 'code': '76'}, {'name': 'Cultural Facilities', 'code': '78'},
                     {'name': 'Festivals and Performances', 'code': '85'},
                     {'name': 'Sports and Recreation', 'code': '75'}, {'name': 'Accommodations', 'code': '80'},
                     {'name': 'Shopping', 'code': '79'}, {'name': 'Restaurants', 'code': '82'},
                     {'name': 'All', 'code': ''}]

    return content_types