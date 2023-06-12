import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from PIL import ImageTk, Image
import requests
from io import BytesIO
import kor_api as kor
import eng_api as eng
from map_api import *
from telegram import Bot
import asyncio
import spam

zoom = 13
language = kor
selected_tourism_info = None
selected_bookmark = None
bookmarks = []
select_map = selected_tourism_info

def start_GUI():
    def kor_clicked():
        global language

        language = kor

        window.destroy()

    def eng_clicked():
        global language

        language = eng

        window.destroy()


    window = tk.Tk()
    window.geometry("400x250")
    window.title("한국관광정보")

    custom_font = font.Font(family="Arial", size=15)

    kor_button = tk.Button(window, text='한국어', command=kor_clicked, width=17, height=10, font=custom_font)
    kor_button.grid(column=0, row=0)
    eng_button = tk.Button(window, text='English', command=eng_clicked, width=17, height=10, font=custom_font)
    eng_button.grid(column=1, row=0)

    window.mainloop()

def mainGUI():

    def graph_draw(sido_code, sigungu_code):
        code12, code14, code15, code28, code32, code38, code39 = 0, 0, 0, 0, 0, 0, 0
        tour_infoes = language.Area_Based(1,'',sido_code,sigungu_code)

        graph_canvas.delete('all')
        if language == kor:
            for tour_info in tour_infoes:
                if tour_info['contenttypeid'] == '12':
                    code12 += 1
                elif tour_info['contenttypeid'] == '14':
                    code14 += 1
                elif tour_info['contenttypeid'] == '15':
                    code15 += 1
                elif tour_info['contenttypeid'] == '28':
                    code28 += 1
                elif tour_info['contenttypeid'] == '32':
                    code32 += 1
                elif tour_info['contenttypeid'] == '38':
                    code38 += 1
                elif tour_info['contenttypeid'] == '39':
                    code39 += 1
        else:
            for tour_info in tour_infoes:
                if tour_info['contenttypeid'] == '76':
                    code12 += 1
                elif tour_info['contenttypeid'] == '78':
                    code14 += 1
                elif tour_info['contenttypeid'] == '85':
                    code15 += 1
                elif tour_info['contenttypeid'] == '75':
                    code28 += 1
                elif tour_info['contenttypeid'] == '80':
                    code32 += 1
                elif tour_info['contenttypeid'] == '79':
                    code38 += 1
                elif tour_info['contenttypeid'] == '82':
                    code39 += 1

        if language == kor:
            content_names = ['관광지', '문화시설', '축제공연행사', '레포츠', '숙박', '쇼핑', '음식점']
        else:
            content_names = ['Tourist Attractions', 'Cultural Facilities', 'Festivals and Performances',
                             'Sports and Recreation', 'Accommodations', 'Shopping', 'Restaurants']

        content_counts = [code12, code14, code15, code28, code32, code38, code39]

        count_sum = spam.spam_plus(content_counts)

        max_content_count = max(content_counts)
        bar_width = 20
        x_gap = 30
        x0 = 20
        y0 = 250
        for i in range(7):
            x1 = x0 + i * (bar_width + x_gap)
            y1 = y0 - 200 * content_counts[i] / max_content_count
            graph_canvas.create_rectangle(x1, y1, x1 + bar_width, y0, fill='blue')
            graph_canvas.create_text(x1 + bar_width / 2, y0 + 100, text=content_names[i], anchor='n', angle=90)
            graph_canvas.create_text(x1 + bar_width / 2, y1 - 10, text=content_counts[i], anchor='s')
        if language == kor:
            graph_canvas.create_text(280, 390, text="합계= "+str(count_sum), anchor='nw')
        else:
            graph_canvas.create_text(280, 390, text="Total= " + str(count_sum), anchor='nw')

    async def telegram():
        global selected_bookmark
        TOKEN = '6187417159:AAEoGlZFKzb1l_6ydyoSPRq4zuPSOyxxbrA'

        bot = Bot(token=TOKEN)
        chat_id = '6048145248'

        for bookmark in selected_bookmark:
            message = f"{bookmark['title']}\n"+f"{bookmark['address']}"
            photo = bookmark['firstimage']
            await bot.send_photo(chat_id=chat_id, photo=photo)
            await bot.send_message(chat_id=chat_id, text=message)

    def telegram_clicked():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(telegram())
        loop.close()

    def bookmark_append():
        global selected_tourism_info
        global selected_bookmark
        global bookmarks

        bookmark_list.delete(0, tk.END)

        tour_infoes = selected_tourism_info
        index = tourism_list.curselection()
        bookmarks.append(tour_infoes[index[0]])

        for bookmark in bookmarks:
            bookmark_list.insert(tk.END, f"{bookmark['title']}")

        selected_bookmark = bookmarks



    def bookmark_delete():
        global selected_bookmark
        global bookmarks

        index = bookmark_list.curselection()

        if index:
            selected_indexes = list(index)
            selected_indexes.sort(reverse=True)
            for idx in selected_indexes:
                bookmarks.pop(idx)

        bookmark_list.delete(0, tk.END)

        for bookmark in bookmarks:
            bookmark_list.insert(tk.END, f"{bookmark['title']}")

        selected_bookmark = bookmarks


    def show_tourism_info(event):
        global selected_tourism_info
        global zoom

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

        detail_infoes = language.Detail_Search(tour_infoes[index[0]]['contentid'])
        overview_text = detail_infoes[0]['overview'].replace("<br>", "")

        info_canvas.create_text(175, 300, text="["+tour_infoes[index[0]]['title']+"]", font=("Georgia", 14, "bold"), width=350)
        info_canvas.create_text(175, 380, text=tour_infoes[index[0]]['address'], font=("Georgia", 13, "bold"), width=350)
        info_canvas.create_text(175, 420, text=detail_infoes[0]['tel'], font=("Georgia", 13, "bold"), width=350)
        info_canvas.create_text(0, 450, text=" "+overview_text, font=("Georgia", 12), width=350, anchor="nw")

        info_canvas.configure(scrollregion=info_canvas.bbox("all"))

        show_map(selected_tourism_info)

    def bookmark_tourism_info(event):
        global selected_bookmark
        global zoom

        info_canvas.delete('all')

        index = bookmark_list.curselection()
        tour_infoes = selected_bookmark

        if tour_infoes[index[0]]['firstimage']:
            img_url = tour_infoes[index[0]]['firstimage']

            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))

            image = image.resize((350, 261))
            photo = ImageTk.PhotoImage(image)

            info_canvas.create_image(0, 0, anchor="nw", image=photo)
            info_canvas.image = photo

        detail_infoes = language.Detail_Search(tour_infoes[index[0]]['contentid'])
        overview_text = detail_infoes[0]['overview'].replace("<br>", "")

        info_canvas.create_text(175, 300, text="["+tour_infoes[index[0]]['title']+"]", font=("Georgia", 14, "bold"), width=350)
        info_canvas.create_text(175, 340, text=tour_infoes[index[0]]['address'], font=("Georgia", 13, "bold"), width=350)
        info_canvas.create_text(175, 360, text=detail_infoes[0]['tel'], font=("Georgia", 13, "bold"), width=350)
        info_canvas.create_text(0, 400, text=" "+overview_text, font=("Georgia", 12), width=350, anchor="nw")

        info_canvas.configure(scrollregion=info_canvas.bbox("all"))

        show_map(selected_bookmark)

    def show_map(select):
        global zoom
        global select_map

        select_map = select

        map_canvas.delete('all')

        tour_infoes = select

        if select == selected_tourism_info:
            index = tourism_list.curselection()
        elif select == selected_bookmark:
            index = bookmark_list.curselection()

        lat = tour_infoes[index[0]]['lat']
        lng = tour_infoes[index[0]]['lng']
        map_photo = Map_Update(lat, lng, zoom)
        map_canvas.create_image(0, 0, anchor="nw", image=map_photo)
        map_canvas.image = map_photo

    def zoom_in():
        global zoom
        global select_map

        zoom += 1
        show_map(select_map)

    def zoom_out():
        global zoom
        global select_map

        if zoom > 1:
            zoom -= 1
        show_map(select_map)


    # 시도 선택에 따른 시군구 업데이트
    def update_sigungu_combo(event):
        selected_name = sido_combo.get()
        selected_code = None

        for sido in area_codes:
            if sido["name"] == selected_name:
                selected_code = sido["code"]
                break

        sigungu_codes = language.Sigungu_Code(selected_code)

        sigungu_options = set([sigungu["name"] for sigungu in sigungu_codes])
        sigungu_combo['values'] = list(sigungu_options)
        if language == kor:
            sigungu_combo.set("시/군/구")
        else:
            sigungu_combo.set("city/county/district")

    def show_tourism_list():
        global selected_tourism_info
        tourism_list.delete(0, tk.END)

        content_name = selected_content.get()
        content = [content for content in content_codes if content['name'] == content_name]
        if content[0]['name'] == '전체' or content[0]['name'] == 'All':
            content_code = None
        else:
            content_code = int(content[0]['code'])

        sido_name = selected_sido.get()
        sido_code_info = [sido_code_info for sido_code_info in area_codes if sido_code_info['name'] == sido_name]
        sido_code = int(sido_code_info[0]['code'])

        sigungu_codes = language.Sigungu_Code(sido_code)
        sigungu_name = selected_sigungu.get()
        sigungu_code_info = [sigungu_code_info for sigungu_code_info in sigungu_codes if sigungu_code_info['name'] == sigungu_name]
        sigungu_code = int(sigungu_code_info[0]['code'])

        tour_infoes = language.Area_Based(1, content_code, sido_code, sigungu_code)

        graph_draw(sido_code, sigungu_code)

        # 캔버스 초기화
        info_canvas.delete('all')

        for tour_info in tour_infoes:
            tourism_list.insert(tk.END, f"{tour_info['title']}")

        selected_tourism_info = tour_infoes

    def canvas_mousewheel(event):
        info_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    window = tk.Tk()

    window.geometry("800x500")
    if language == kor:
        window.title("한국관광정보")
    else:
        window.title("Korea Tourism Information")

    # 프레임 생성
    frame1 = tk.Frame(width=400, height=500, relief="solid")
    frame1.place(x=0, y=0)
    frame2 = tk.Frame(width=400, height=500, relief="solid")
    frame2.place(x=400, y=0)

    # 지역 선택 라벨
    if language == kor:
        label1 = tk.Label(frame1, text="지역 선택")
    else:
        label1 = tk.Label(frame1, text="Select a region")
    label1.grid(column=0, row=0, sticky="w")

    if language == kor:
        label2 = tk.Label(frame1, text="관광 유형 분류")
    else:
        label2 = tk.Label(frame1, text="Classification of tourism types")
    label2.grid(column=0, row=2, sticky="w")

    # 지역 선택 콤보 박스
    area_codes = language.Area_Code()
    selected_sido = tk.StringVar()
    if language == kor:
        selected_sido.set("시/도")
    else:
        selected_sido.set("State/Province")
    sido_options = set([sido["name"] for sido in area_codes])
    sido_combo = ttk.Combobox(frame1, textvariable=selected_sido, values=list(sido_options))
    sido_combo.grid(column=0, row=1)

    selected_sigungu = tk.StringVar()
    if language == kor:
        selected_sigungu.set("시/군/구")
    else:
        selected_sigungu.set("city/county/district")
    sigungu_options = set([])
    sigungu_combo = ttk.Combobox(frame1, textvariable=selected_sigungu, values=list(sigungu_options))
    sigungu_combo.grid(column=1, row=1)

    content_codes = language.Content_Type()
    selected_content = tk.StringVar()
    if language == kor:
        selected_content.set("전체")
    else:
        selected_content.set("All")
    content_options = set([content["name"] for content in content_codes])
    content_combo = ttk.Combobox(frame1, textvariable=selected_content, values=list(content_options))
    content_combo.grid(column=0, row=3)

    if language == kor:
        search_button = tk.Button(frame1, text=' 검색 ', command=show_tourism_list)
    else:
        search_button = tk.Button(frame1, text=' Search ', command=show_tourism_list)
    search_button.grid(column=1, row=3, sticky='w')

    sido_combo.bind("<<ComboboxSelected>>", update_sigungu_combo)

    # Notebook1 생성
    notebook1 = ttk.Notebook(frame1)
    notebook1.grid(column=0, row=4, columnspan=2)

    # 검색결과 리스트 박스 (tab1)
    n1_tab1 = ttk.Frame(notebook1)
    tourism_list = tk.Listbox(n1_tab1, width=50, height=20)
    tourism_list.grid(column=0, row=0)
    if language == kor:
        notebook1.add(n1_tab1, text='검색결과')
    else:
        notebook1.add(n1_tab1, text='Search Results')

    # 즐겨찾기 리스트 박스 (tab2)
    n1_tab2 = ttk.Frame(notebook1)
    bookmark_list = tk.Listbox(n1_tab2, width=50, height=20)
    bookmark_list.grid(column=0, row=0)
    if language == kor:
        notebook1.add(n1_tab2, text='즐겨찾기')
    else:
        notebook1.add(n1_tab2, text='Bookmark')

    # 검색결과 스크롤바
    scrollbar1 = tk.Scrollbar(n1_tab1, orient="vertical")
    scrollbar1.grid(column=1, row=0, sticky="NS")
    # 즐겨찾기 스크롤바
    scrollbar2 = tk.Scrollbar(n1_tab2, orient="vertical")
    scrollbar2.grid(column=1, row=0, sticky="NS")

    # 스크롤바와 검색결과 연결
    tourism_list.config(yscrollcommand=scrollbar1.set)
    scrollbar1.config(command=tourism_list.yview)
    # 스크롤바와 즐겨찾기 연결
    bookmark_list.config(yscrollcommand=scrollbar2.set)
    scrollbar2.config(command=bookmark_list.yview)

    # 즐겨찾기 추가, 삭제 버튼 생성
    if language == kor:
        bookmark_add_button = tk.Button(frame1, text="즐겨찾기 추가", command=bookmark_append)
    else:
        bookmark_add_button = tk.Button(frame1, text="Bookmark Append", command=bookmark_append)
    bookmark_add_button.grid(column=0, row=5, sticky="e")
    if language == kor:
        bookmark_del_button = tk.Button(frame1, text="즐겨찾기 삭제", command=bookmark_delete)
    else:
        bookmark_del_button = tk.Button(frame1, text="Bookmakr Delete", command=bookmark_delete)
    bookmark_del_button.grid(column=1, row=5, sticky="w")

    # 텔레그렘 전송 버튼 생성
    telegram_button = tk.Button(frame1, text="Telegram", command=telegram_clicked)
    telegram_button.grid(column=1, row=5, sticky="e")

    # Notebook2 생성
    notebook2 = ttk.Notebook(frame2)
    notebook2.grid(column=0, row=0)

    # 첫번째 탭에 정보창 캔버스 생성
    n2_tab1 = ttk.Frame(notebook2)
    info_canvas = tk.Canvas(n2_tab1, width=350, height=405, background='white')
    info_canvas.grid(column=0, row=1, columnspan=2)
    if language == kor:
        notebook2.add(n2_tab1, text='정보')
    else:
        notebook2.add(n2_tab1, text='Information')

    # 두번째 탭에 지도 캔버스 생성
    n2_tab2 = ttk.Frame(notebook2)
    map_canvas = tk.Canvas(n2_tab2, width=360, height=410)
    map_canvas.grid(column=0, row=1, columnspan=2)
    if language == kor:
        notebook2.add(n2_tab2, text='지도')
    else:
        notebook2.add(n2_tab2, text='Map')

    # 줌인 줌아웃 버튼 생성
    zoom_in_button = tk.Button(n2_tab2, text=" + ", command=zoom_in)
    zoom_in_button.grid(column=0, row=0, sticky='e')
    zoom_out_button = tk.Button(n2_tab2, text=" - ", command=zoom_out)
    zoom_out_button.grid(column=1, row=0, sticky='w')

    # 세번째 탭에 그래프 캔버스 생성
    n2_tab3 = ttk.Frame(notebook2)
    graph_canvas = tk.Canvas(n2_tab3, width=360, height=410, background='white')
    graph_canvas.grid(column=0, row=1, columnspan=2)
    if language == kor:
        notebook2.add(n2_tab3, text='그래프')
    else:
        notebook2.add(n2_tab3, text='Graph')

    # 정보창 스크롤바
    scrollbar2 = tk.Scrollbar(n2_tab1, orient="vertical")
    scrollbar2.grid(column=2, row=1, sticky="NS")

    # 스크롤바와 캔버스 연결
    info_canvas.config(yscrollcommand=scrollbar2.set)
    scrollbar2.config(command=info_canvas.yview)

    tourism_list.bind("<<ListboxSelect>>", show_tourism_info)
    bookmark_list.bind("<<ListboxSelect>>", bookmark_tourism_info)
    info_canvas.bind("<MouseWheel>", canvas_mousewheel)

    window.mainloop()


start_GUI()
mainGUI()