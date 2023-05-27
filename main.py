import tkinter as tk
import tkinter.ttk as ttk
import requests
import xml.etree.ElementTree as ET
from kor_api import *

def mainGUI():

    def update_sigungu_combo(event):
        selected_name = sido_combo.get()
        selected_code = None

        for sido in area_codes:
            if sido["name"] == selected_name:
                selected_code = sido["code"]
                break

        sigungu_codes = Sigungu_Code(selected_code)

        sigungu_options = set([sigungu["name"] for sigungu in sigungu_codes])
        sigungu_combo['values'] = list(sigungu_options)
        sigungu_combo.set("시/군/구")



    window = tk.Tk()

    window.geometry("1000x500")
    window.title("한국관광정보")

    label1 = tk.Label(window, text="지역 선택")
    label1.grid(column=0, row=0, sticky="w")

    label2 = tk.Label(window, text="관광 유형 분류")
    label2.grid(column=0, row=2, sticky="w")

    area_codes = Area_Code()

    selected_sido = tk.StringVar()
    selected_sido.set("시/도")
    sido_options = set([sido["name"] for sido in area_codes])
    sido_combo = ttk.Combobox(window, textvariable=selected_sido, values=list(sido_options))
    sido_combo.grid(column=0, row=1)
    print(selected_sido)

    selected_sigungu = tk.StringVar()
    selected_sigungu.set("시/군/구")
    sigungu_options = set([])
    sigungu_combo = ttk.Combobox(window, textvariable=selected_sigungu, values=list(sigungu_options))
    sigungu_combo.grid(column=1, row=1)

    selected_category = tk.StringVar()
    selected_category.set("전체")
    category_options = set([])
    category_combo = ttk.Combobox(window, textvariable=selected_category, value=list(category_options))
    category_combo.grid(column=0, row=3)

    sido_combo.bind("<<ComboboxSelected>>", update_sigungu_combo)


    window.mainloop()


mainGUI()