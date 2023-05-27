import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import requests
from io import BytesIO
from kor_api import *


def mainGUI():

    selected_tourism_info = None

    def show_tourism_info(event):
        global selected_tourism_info

        info_canvas.delete('all')

        index = tourism_list.curselection()
        tour_infoes = selected_tourism_info

        if tour_infoes[index[0]]['firstimage']:
            img_url = tour_infoes[index[0]]['firstimage']

            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))

            image = image.resize((350, 261))
            photo = ImageTk.PhotoImage(image)

            info_canvas.create_image(0, 0, anchor="nw", image=photo)
            info_canvas.image = photo

        info_canvas.create_text(175, 330, text=tour_infoes[index[0]]['title'], font=("Arial", 10), width=350)
        info_canvas.create_text(175, 350, text="주소:"+tour_infoes[index[0]]['address'], font=("Arial", 10), width=350)



    # 시도 선택에 따른 시군구 업데이트
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

    def show_tourism_list(event):
        global selected_tourism_info
        tourism_list.delete(0, tk.END)

        content_name = selected_content.get()
        content = [content for content in content_codes if content['name'] == content_name]
        if content[0]['name'] == '전체':
            content_code = None
        else:
            content_code = int(content[0]['code'])

        sido_name = selected_sido.get()
        sido_code_info = [sido_code_info for sido_code_info in area_codes if sido_code_info['name'] == sido_name]
        sido_code = int(sido_code_info[0]['code'])

        sigungu_codes = Sigungu_Code(sido_code)
        sigungu_name = selected_sigungu.get()
        sigungu_code_info = [sigungu_code_info for sigungu_code_info in sigungu_codes if sigungu_code_info['name'] == sigungu_name]
        sigungu_code = int(sigungu_code_info[0]['code'])

        tour_infoes = Area_Based(1, content_code, sido_code, sigungu_code)

        tourism_title = [tourism['title'] for tourism in tour_infoes]

        # 캔버스 초기화
        info_canvas.delete('all')

        for tour_info in tour_infoes:
            tourism_list.insert(tk.END, f"{tour_info['title']}")

        selected_tourism_info = tour_infoes


    window = tk.Tk()

    window.geometry("800x500")
    window.title("한국관광정보")

    # 프레임 생성
    frame1 = tk.Frame(width=400, height=500, relief="solid")
    frame1.place(x=0, y=0)
    frame2 = tk.Frame(width=400, height=500, relief="solid")
    frame2.place(x=400, y=0)

    # 지역 선택 라벨
    label1 = tk.Label(frame1, text="지역 선택")
    label1.grid(column=0, row=0, sticky="w")

    label2 = tk.Label(frame1, text="관광 유형 분류")
    label2.grid(column=0, row=2, sticky="w")

    # 지역 선택 콤보 박스
    area_codes = Area_Code()
    selected_sido = tk.StringVar()
    selected_sido.set("시/도")
    sido_options = set([sido["name"] for sido in area_codes])
    sido_combo = ttk.Combobox(frame1, textvariable=selected_sido, values=list(sido_options))
    sido_combo.grid(column=0, row=1)

    selected_sigungu = tk.StringVar()
    selected_sigungu.set("시/군/구")
    sigungu_options = set([])
    sigungu_combo = ttk.Combobox(frame1, textvariable=selected_sigungu, values=list(sigungu_options))
    sigungu_combo.grid(column=1, row=1)

    content_codes = Content_Type()
    selected_content = tk.StringVar()
    selected_content.set("전체")
    content_options = set([content["name"] for content in content_codes])
    content_combo = ttk.Combobox(frame1, textvariable=selected_content, values=list(content_options))
    content_combo.grid(column=0, row=3)

    sido_combo.bind("<<ComboboxSelected>>", update_sigungu_combo)

    # 목록 라벨
    label3 = tk.Label(frame1, text="목록")
    label3.grid(column=0, row=4, sticky="w")

    # 목록 리스트 박스
    tourism_list = tk.Listbox(frame1, width=50, height=20)
    tourism_list.grid(column=0, row=5, columnspan=2)

    # 목록 스크롤바
    scrollbar1 = tk.Scrollbar(frame1, orient="vertical")
    scrollbar1.grid(column=2, row=5, sticky="NS")

    # 스크롤바와 목록 연결
    tourism_list.config(yscrollcommand=scrollbar1.set)
    scrollbar1.config(command=tourism_list.yview)

    # 정보창 라벨
    label4 = tk.Label(frame2, text="정보")
    label4.grid(column=0, row=0, sticky="w")

    # 정보창 캔버스
    info_canvas = tk.Canvas(frame2, width=350, height=405, background='white')
    info_canvas.grid(column=0, row=1, columnspan=2)

    scrollbar2 = tk.Scrollbar(frame2, orient="vertical")
    scrollbar2.grid(column=2, row=1, sticky="NS")

    info_canvas.config(yscrollcommand=scrollbar2.set)
    scrollbar2.config(command=info_canvas.yview)

    content_combo.bind("<<ComboboxSelected>>", show_tourism_list)
    tourism_list.bind("<<ListboxSelect>>", show_tourism_info)

    window.mainloop()


mainGUI()