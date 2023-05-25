import tkinter as tk
import tkinter.ttk as ttk
import requests
import xml.etree.ElementTree as ET

# 공공데이터 API 키 (Decoding)
api_key = ""
Keyword = "강원"
encoded_keyword = Keyword.encode("utf-8")
ContentTypeId = 12

url = "http://apis.data.go.kr/B551011/KorService1/searchKeyword1"
params = {
    "numOfRows": 100,
    "MobileOS": "ETC",
    "MobileApp": "Korea_tourism",
    "keyword": encoded_keyword,
    "contentTypeId": ContentTypeId,
    "serviceKey": api_key
}

response = requests.get(url, params=params)
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


def mainGUI():

    def update_combobox2(event):
        select = combo1.get()
        if select == "서울특별시":
            combo2['values'] = ("선택", "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구",
                                "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구",
                                "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구")
        elif select == "부산광역시":
            combo2['values'] = ("시/군 선택", "강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구",
                                "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구")
        elif select == "대구광역시":
            combo2['values'] = ("시/군 선택", "남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구")
        elif select == "인천광역시":
            combo2['values'] = ("시/군 선택", "강화군", "계양구", "남구", "남동구", "동구", "부평구", "서구", "연수구", "웅진군", "중구")
        elif select == "광주광역시":
            combo2['values'] = ("시/군 선택", "광산구", "남구", "동구", "북구", "서구")
        elif select == "대전광역시":
            combo2['values'] = ("시/군 선택", "대덕구", "동구", "서구", "유성구", "중구")
        elif select == "울산광역시":
            combo2['values'] = ("시/군 선택", "남구", "동구", "북구", "울주군", "중구")
        elif select == "세종특별자치시":
            combo2['values'] = ("시/군 선택", "세종시")
        elif select == "경기도":
            combo2['values'] = ("시/군 선택", "가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시",
                                "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시",
                                "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시",
                                "평택시", "포천시", "하남시", "화성시")
        elif select == "강원도":
            combo2['values'] = ("시/군 선택", "강릉시", "고성군", "동해시", "삼척시", "속초시", "속초시", "양구군")
        elif select == "충청북도":
            combo2['values'] = ("시/군 선택", "수원시", "용인시", "성남시", "고양시")
        elif select == "충청남도":
            combo2['values'] = ("시/군 선택", "수원시", "용인시", "성남시", "고양시")
        elif select == "전라북도":
            combo2['values'] = ("시/군 선택", "수원시", "용인시", "성남시", "고양시")
        elif select == "전라남도":
            combo2['values'] = ("시/군 선택", "수원시", "용인시", "성남시", "고양시")
        elif select == "경상북도":
            combo2['values'] = ("시/군 선택", "수원시", "용인시", "성남시", "고양시")
        elif select == "경상남도":
            combo2['values'] = ("시/군 선택", "수원시", "용인시", "성남시", "고양시")
        elif select == "제주특별자치도":
            combo2['values'] = ("시/군 선택", "수원시", "용인시", "성남시", "고양시")

        else:
            combo2['values'] = ("군/구 선택")


    window = tk.Tk()

    window.geometry("1000x500")
    window.title("한국관광정보")

    label1 = tk.Label(window, text="지역 선택")
    label1.grid(column=0, row=0, sticky="w")

    label2 = tk.Label(window, text="관광 유형 분류")
    label2.grid(column=0, row=2, sticky="w")

    combo1 = ttk.Combobox(window)
    combo1['values'] = ("시/도", "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시",
                        "세종특별자치시", "경기도", "강원도", "충청북도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도")
    combo1.current(0)
    combo1.grid(column=0, row=1)

    combo2 = ttk.Combobox(window)
    combo2['values'] = ("시/군/구",)
    combo2.current(0)
    combo2.grid(column=1, row=1)

    combo3 = ttk.Combobox(window)
    combo3['values'] = ("전체", "쇼핑", "공연")
    combo3.current(0)
    combo3.grid(column=0, row=3)

    combo1.bind("<<ComboboxSelected>>", update_combobox2)


    window.mainloop()


mainGUI()