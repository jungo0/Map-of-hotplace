from __future__ import print_function
import operator
import random
import pandas as pd
import numpy as np
import io
import math
import folium
from haversine import haversine
from collections import Counter
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi


global 음식점_csv
global 카페_csv,당구장_csv,pc방_csv,보드게임카페_csv,노래방_csv,방탈출_csv,볼링장_csv,백화점_csv,영화관_csv
global csv_select
global recommend
global recommend2
global Place        #고정 gps
global rating
global check

rating=[]
Place=(37.49811479072191, 127.02765875703757)
check = Counter({"한식":0,"양식":0,"일식":0,"고기집":0,"분식":0,"인도":0,"패스트푸드":0,"중국집":0,"치킨":0})

카페_csv='./csv\\카페_1.csv'
당구장_csv='./csv\\당구장.csv'
pc방_csv='./csv\\PC방.csv'
보드게임카페_csv='./csv\\보드게임카페.csv'
노래방_csv='./csv\\노래방.csv'
방탈출_csv='./csv\\방탈출.csv'
볼링장_csv='./csv\\볼링장.csv'
백화점_csv='./csv\\백화점.csv'
영화관_csv='./csv\\영화관.csv'
음식점_csv='./csv\\음식점.csv'

csv_select=''

class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        form = './main.ui'
        uic.loadUi(form,self)
        self.parent = parent
        self.title_button_1.clicked.connect(self.show_choice1_window)
        self.title_button_2.clicked.connect(self.show_choice2_window)
        self.title_button_3.clicked.connect(self.show_check2_window)
        self.title_close.clicked.connect(self.close)
        self.show()

    def show_check2_window(self):
        self.close()
        self.parent.set_content("check2")

    def show_choice2_window(self):
        self.close()
        self.parent.set_content("choice2")

    def show_choice1_window(self):
        self.close()
        self.parent.set_content("choice1")

class choice1widget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        form = './choice1.ui'
        uic.loadUi(form,self)
        self.setWindowTitle("음식점선택")
        self.parent = parent
        self.button_close.clicked.connect(self.close)
        self.button_main.clicked.connect(self.show_main_window)
        self.button1.clicked.connect(self.choice)
        self.button3.clicked.connect(self.show_check_window)
        self.button_rec.clicked.connect(self.show_recommend)
        self.show()

    def show_recommend(self):
        global s
        s = "추천지도"
        if s == "추천지도":
            pixmap = (QPixmap('./good.png'))
            self.numl.setText(s)
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(250,250)
            self.button_rec2.clicked.connect(self.show_check_window)
            self.label_txt.setText("사용자추천")
            self.show

    def show_main_window(self):
        self.close()
        self.parent.set_content("Main")

    def show_check_window(self):
        self.close()
        self.parent.set_content("check")
    
    def choice(self):
        global s
        list = ["한식","일식","중식","양식","분식","패스트푸드","인도태국","고기집","치킨"]
        s = str(random.choice(list))
        self.numl.setText(s)

        if s == "한식":
            pixmap = (QPixmap('./image\\한식.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("닭갈비,된장찌개")
            self.show
        if s == "일식":
            pixmap = (QPixmap('./image\\일식.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("스시,우동,가츠동")
            self.show
        if s == "중식":
            pixmap = (QPixmap('./image\\중국집.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("짜장면,마라탕,양꼬치")
            self.show
        if s == "양식":
            pixmap = (QPixmap('./image\\양식.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("피자,파스타,스테이크")
            self.show
        if s == "분식":
            pixmap = (QPixmap('./image\\분식.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("떡볶이,김밥,컵밥")
            self.show
        if s == "패스트푸드":
            pixmap = (QPixmap('./image\\패스트푸드.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("햄버거,샌드위치")
            self.show
        if s == "인도태국":
            pixmap = (QPixmap('./image\\인도.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("카레,팟타이")
            self.show
        if s == "고기집":
            pixmap = (QPixmap('./image\\고기집.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("삼겹살,돼지갈비,소고기")
            self.show
        if s == "치킨":
            pixmap = (QPixmap('./image\\치킨.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("뿌링클,허니콤보")
            self.show

class choice2widget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        form = './choice2.ui'
        uic.loadUi(form,self)
        self.setWindowTitle("장소선택")
        self.parent = parent
        self.button_close.clicked.connect(self.close)
        self.button_main.clicked.connect(self.show_main_window)
        self.button1.clicked.connect(self.choice)
        self.show()

    def choice(self):
        global s
        list = ["노래방","당구장","방탈출","백화점","보드게임카페","볼링장","영화관","카페","PC방"]
        s = str(random.choice(list))
        self.numl.setText(s)

        if s == "노래방":
            pixmap = (QPixmap('./image_2\\노래방.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("스트레스를 해소하고 싶다면?!")
            self.show
        if s == "당구장":
            pixmap = (QPixmap('./image_2\\당구장.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("친구들과 내기 한 판?")
            self.show
        if s == "방탈출":
            pixmap = (QPixmap('./image_2\\방탈출.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("내가 바로 탈출왕!")
            self.show
        if s == "백화점":
            pixmap = (QPixmap('./image_2\\백화점.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("오늘하루 Flex~")
            self.show
        if s == "보드게임카페":
            pixmap = (QPixmap('./image_2\\보드게임.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("여러가지 게임을 동시에!")
            self.show
        if s == "볼링장":
            pixmap = (QPixmap('./image_2\\볼링장.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("볼 좀 굴려볼까?")
            self.show
        if s == "영화관":
            pixmap = (QPixmap('./image_2\\영화관.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("영화 한 편은 어때")
            self.show
        if s == "카페":
            pixmap = (QPixmap('./image_2\\카페.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("커피 한 잔 할래요~")
            self.show
        if s == "PC방":
            pixmap = (QPixmap('./image_2\\pc방.png'))
            self.label_img.setPixmap(QPixmap(pixmap))
            self.label_img.resize(230,230)
            self.button3.clicked.connect(self.show_check_window)
            self.label_txt.setText("오늘 하루는 여기서!")
            self.show

    def show_check_window(self):
        self.close()
        self.parent.set_content("check")

    def show_main_window(self):
        self.close()
        self.parent.set_content("Main")

global MAX_1


class choice3widget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        form = './choice3.ui'
        uic.loadUi(form,self)
        self.setWindowTitle("음식점선택")
        self.parent = parent
        self.button_close.clicked.connect(self.close)
        self.button_main.clicked.connect(self.show_main_window)
        self.button1.clicked.connect(self.choice)
        self.show()
    
    def choice(self):
            global s
            s = MAX_1
            self.numl.setText(s)
            if s == "한식":
                pixmap = (QPixmap('./image\\한식.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("닭갈비,된장찌개")
                self.show
            if s == "일식":
                pixmap = (QPixmap('./image\\일식.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("스시,우동,가츠동")
                self.show
            if s == "중식":
                pixmap = (QPixmap('./image\\중국집.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("짜장면,마라탕,양꼬치")
                self.show
            if s == "양식":
                pixmap = (QPixmap('./image\\양식.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("피자,파스타,스테이크")
                self.show
            if s == "분식":
                pixmap = (QPixmap('./image\\분식.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("떡볶이,김밥,컵밥")
                self.show
            if s == "패스트푸드":
                pixmap = (QPixmap('./image\\패스트푸드.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("햄버거,샌드위치")
                self.show
            if s == "인도태국":
                pixmap = (QPixmap('./image\\인도.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("카레,팟타이")
                self.show
            if s == "고기집":
                pixmap = (QPixmap('./image\\고기집.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("삼겹살,돼지갈비,소고기")
                self.show
            if s == "치킨":
                pixmap = (QPixmap('./image\\치킨.png'))
                self.label_img.setPixmap(QPixmap(pixmap))
                self.label_img.resize(230,230)
                self.button3.clicked.connect(self.show_check_window)
                self.label_txt.setText("뿌링클,허니콤보")
                self.show
    def show_check_window(self):
        self.close()
        self.parent.set_content("check")

    def show_main_window(self):
        self.close()
        self.parent.set_content("Main")

class check2widget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        form = './check2.ui'
        uic.loadUi(form,self)
        self.setWindowTitle("음식추천")
        self.parent = parent
        self.button_close.clicked.connect(self.close)
        self.button_main.clicked.connect(self.show_main_window)
        self.button_1.clicked.connect(self.show_choice3)
        self.time_1.stateChanged.connect(self.checkBoxState)
        self.time_2.stateChanged.connect(self.checkBoxState)
        self.time_3.stateChanged.connect(self.checkBoxState)
        self.with_1.stateChanged.connect(self.checkBoxState)
        self.with_2.stateChanged.connect(self.checkBoxState)
        self.with_3.stateChanged.connect(self.checkBoxState)
        self.easy_1.stateChanged.connect(self.checkBoxState)
        self.easy_2.stateChanged.connect(self.checkBoxState)
        self.qus_1.stateChanged.connect(self.checkBoxState)
        self.qus_2.stateChanged.connect(self.checkBoxState)
        self.qus_3.stateChanged.connect(self.checkBoxState)
        self.money_1.stateChanged.connect(self.checkBoxState)
        self.money_2.stateChanged.connect(self.checkBoxState)
        self.money_3.stateChanged.connect(self.checkBoxState)
        self.hot_1.stateChanged.connect(self.checkBoxState)
        self.hot_2.stateChanged.connect(self.checkBoxState)
        self.food_1.stateChanged.connect(self.checkBoxState)
        self.food_2.stateChanged.connect(self.checkBoxState)
        self.food_3.stateChanged.connect(self.checkBoxState)
        self.food_4.stateChanged.connect(self.checkBoxState)
        self.food_5.stateChanged.connect(self.checkBoxState)
        self.food_6.stateChanged.connect(self.checkBoxState)
        self.food_7.stateChanged.connect(self.checkBoxState)
        self.food_8.stateChanged.connect(self.checkBoxState)
        self.food_9.stateChanged.connect(self.checkBoxState)
        self.show()
    
        

    def checkBoxState(self,state):
        global MAX_1
        check2 = Counter({"한식":0,"양식":0,"일식":0,"고기집":0,"분식":0,"인도":0,"패스트푸드":0,"중국집":0,"치킨":0})
        check3 = Counter({"한식":0,"양식":0,"일식":0,"고기집":0,"분식":0,"인도":0,"패스트푸드":0,"중국집":0,"치킨":0})
        check4 = Counter({"한식":0,"양식":0,"일식":0,"고기집":0,"분식":0,"인도":0,"패스트푸드":0,"중국집":0,"치킨":0})
        check5 = Counter({"한식":0,"양식":0,"일식":0,"고기집":0,"분식":0,"인도":0,"패스트푸드":0,"중국집":0,"치킨":0})
        check6 = Counter({"한식":0,"양식":0,"일식":0,"고기집":0,"분식":0,"인도":0,"패스트푸드":0,"중국집":0,"치킨":0})
        check7 = Counter({"한식":0,"양식":0,"일식":0,"고기집":0,"분식":0,"인도":0,"패스트푸드":0,"중국집":0,"치킨":0})
        check["한식"]=0
        check["양식"]=0
        check["일식"]=0
        check["중국집"]=0
        check["고기집"]=0
        check["패스트푸드"]=0
        check["분식"]=0
        check["인도"]=0
        check["치킨"]=0
        if self.time_1.isChecked()==True:
            check["한식"]+=1
        if self.time_2.isChecked()==True:
            check["한식"]+=1
            check["일식"]+=1
            check["분식"]+=1
            check["인도"]+=1
            check["패스트푸드"]+=1
            check["중국집"]+=1
            check["치킨"]+=1
        if self.time_3.isChecked()==True:
            check["양식"]+=1
            check["인도"]+=1
            check["패스트푸드"]+=1
            check["중국집"]+=1
            check["치킨"]+=1
        check2["한식"]=0
        check2["양식"]=0
        check2["일식"]=0
        check2["중국집"]=0
        check2["고기집"]=0
        check2["패스트푸드"]=0
        check2["분식"]=0
        check2["인도"]=0
        check2["치킨"]=0

        if self.easy_1.isChecked()==True:
            check2["한식"]+=1
            check2["패스트푸드"]+=1
            check2["분식"]+=1
        if self.easy_2.isChecked()==True:
            check2["양식"]+=1
            check2["일식"]+=1
            check2["고기집"]+=1
            check2["인도"]+=1
            check2["중국집"]+=1
            check2["치킨"]+=1
        check3["한식"]=0
        check3["양식"]=0
        check3["일식"]=0
        check3["중국집"]=0
        check3["고기집"]=0
        check3["패스트푸드"]=0
        check3["분식"]=0
        check3["인도"]=0
        check3["치킨"]=0
    
        if self.with_1.isChecked()==True:
            check3["한식"]+=1
            check3["양식"]+=1
            check3["중국집"]+=1
            check3["고기집"]+=1
        if self.with_2.isChecked()==True:
            check3["치킨"]+=1
            check3["양식"]+=1
            check3["일식"]+=1
            check3["고기집"]+=1
        if self.with_3.isChecked()==True:
            check3["패스트푸드"]+=1
            check3["분식"]+=1
        check4["한식"]=0
        check4["양식"]=0
        check4["일식"]=0
        check4["중국집"]=0
        check4["고기집"]=0
        check4["패스트푸드"]=0
        check4["분식"]=0
        check4["인도"]=0
        check4["치킨"]=0
       
        if self.qus_1.isChecked()==True:
            check4["한식"]+=1
        if self.qus_2.isChecked()==True:
            check4["한식"]+=1
            check4["인도"]+=1
            check4["일식"]+=1
        if self.qus_3.isChecked()==True:
            check4["양식"]+=1
            check4["일식"]+=1
            check4["중국집"]+=1
            check4["고기집"]+=1
            check4["패스트푸드"]+=1
            check4["분식"]+=1
        check5["한식"]=0
        check5["양식"]=0
        check5["일식"]=0
        check5["중국집"]=0
        check5["고기집"]=0
        check5["패스트푸드"]=0
        check5["분식"]=0
        check5["인도"]=0
        check5["치킨"]=0

        if self.money_1.isChecked()==True:
            check5["분식"]+=1
            check5["패스트푸드"]+=1
        if self.money_2.isChecked()==True:
            check5["일식"]+=1
            check5["한식"]+=1
            check5["양식"]+=1
            check5["인도"]+=1
        if self.money_3.isChecked()==True:
            check5["일식"]+=1
            check5["고기집"]+=1
            check5["양식"]+=1
            check5["치킨"]+=1
        check6["한식"]=0
        check6["양식"]=0
        check6["일식"]=0
        check6["중국집"]=0
        check6["고기집"]=0
        check6["패스트푸드"]=0
        check6["분식"]=0
        check6["인도"]=0
        check6["치킨"]=0

        if self.hot_1.isChecked()==True:
            check6["분식"]+=1
            check6["한식"]+=1
            check6["인도"]+=1
            check6["치킨"]+=1
            check6["중국집"]+=1
        if self.hot_2.isChecked()==True:
            check6["일식"]+=1
            check6["고기집"]+=1
            check6["양식"]+=1
            check6["패스트푸드"]+=1
        check7["한식"]=0
        check7["양식"]=0
        check7["일식"]=0
        check7["중국집"]=0
        check7["고기집"]=0
        check7["패스트푸드"]=0
        check7["분식"]=0
        check7["인도"]=0
        check7["치킨"]=0
        if self.food_1.isChecked()==True:
            check7["한식"]=1
        if self.food_2.isChecked()==True:
            check7["양식"]=1
        if self.food_3.isChecked()==True:
            check7["일식"]=1
        if self.food_4.isChecked()==True:
            check7["고기집"]=1
        if self.food_5.isChecked()==True:
            check7["분식"]=1
        if self.food_6.isChecked()==True:
            check7["인도"]=1
        if self.food_7.isChecked()==True:
            check7["패스트푸드"]=1
        if self.food_8.isChecked()==True:
            check7["중국집"]=1
        if self.food_9.isChecked()==True:
            check7["치킨"]=1

        total = check+check2+check3+check4+check5+check6+check7
        print(total)
        MAX_1 = max(total.items(), key=operator.itemgetter(1))[0]
        print(MAX_1)

        self.scrollArea.setStyleSheet("/* VERTICAL SCROLLBAR */\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    \n"
"    background-color: rgb(248, 248, 248);\n"
"    width: 14px;\n"
"    margin: 15px 0 15px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"\n"
"/*  HANDLE BAR VERTICAL */\n"
"QScrollBar::handle:vertical {    \n"
"    background-color: rgba(85, 170, 127, 50);\n"
"    min-height: 30px;\n"
"    border-radius: 7px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{    \n"
"    \n"
"    background-color: rgba(85, 170, 127, 120);\n"
"}\n"
"QScrollBar::handle:vertical:pressed {    \n"
"    \n"
"    background-color: rgba(85, 170, 127, 170);\n"
"}\n"
"\n"
"/* BTN TOP - SCROLLBAR */\n"
"QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    \n"
"    background-color: rgba(30, 91, 44,210);\n"
"    height: 0px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius:0px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical:hover {    \n"
"    background-color: rgb(255, 0, 127);\n"
"}\n"
"QScrollBar::sub-line:vertical:pressed {    \n"
"    background-color: rgb(255, 0, 127);\n"
"}\n"
"\n"
"/* BTN BOTTOM - SCROLLBAR */\n"
"QScrollBar::add-line:vertical {\n"
"    border: none;\n"
"    background-color: rgb(59, 59, 90);\n"
"    height: 0px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical:hover {    \n"
"    background-color: rgb(255, 0, 127);\n"
"}\n"
"QScrollBar::add-line:vertical:pressed {    \n"
"    background-color: rgb(185, 0, 92);\n"
"}\n"
"\n"
"/* RESET ARROW */\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"\n"
"\n"
"/* HORIZONTAL SCROLLBAR - HOMEWORK */\n"
"QScrollBar:horizontal {\n"
"   \n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    \n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    \n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    \n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"\n"
"}")
    def show_main_window(self):
        self.close()
        self.parent.set_content("Main")
    
    def show_choice3(self):
        self.close()
        self.parent.set_content("choice3")

class checkwidget(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent):
        global dataset
        dataset=pd.read_csv('./csv\\음식점카운트.csv',encoding='cp949')
        super().__init__()
        self.parent = parent
        self.setWindowTitle("추천지도")
        self.setWindowIcon(QIcon("./good.png"))
        
        def select():

            rating=[]
            for i in range(0,999):
                try:
                    rating.append(dataset.iloc[0][i])
                except:
                    break
            rating.sort()
            rating=rating[::-1]
            rating2=[]
            for i in range(0,999):
                try:
                    if dataset.iloc[0][i]>= rating[1]:
                        rating2.append(dataset.columns[i])
                except:
                    break
           
            dataset['recommend']=rating2[0]
            dataset['recommend2']=rating2[1]
            return rating2

        def star_rate(list):
            rating=[]
            for path in df['kakao_star']:
                if path<=5 and path>=4.5:
                    path=25
                elif path<4 and path>=3.5:
                    path=22
                elif path<3.5 and path>=3:
                    path=19
                elif path<3 and path>=2.5:
                    path=16
                elif path<2.5 and path>=2:
                    path=13
                elif path<2 and path>=1.5:
                    path=10
                elif path<1.5 and path>=1:
                    path=7
                elif path<1 and path>=0.5:
                    path=4
                else:
                    path=0
                rating.append(path)
            df['rate']=rating

        def star_nums(list):
            rating=[]
            for path in df['kakao_star_nums']:
                if str(path)>str(100):
                    path=25
                elif str(path)<str(100) and str(path)>=str(90):
                    path=22
                elif str(path)<str(90) and str(path)>=str(80):
                    path=19
                elif str(path)<str(70) and str(path)>=str(60):
                    path=16
                elif str(path)<str(60) and str(path)>=str(50):
                    path=13
                elif str(path)<str(50) and str(path)>=str(40):
                    path=10
                elif str(path)<str(40) and str(path)>=str(30):
                    path=7
                elif str(path)<str(30) and str(path)>=str(20):
                    path=4
                else:
                    path=0
                rating.append(path)
            df['rate2']=rating

        def kakao_blog_review(list):
            rating=[]
            for path in df['kakao_blog_review']:
                if str(path)>str(100):
                    path=25
                elif str(path)<str(100) and str(path)>=str(90):
                    path=22
                elif str(path)<str(90) and str(path)>=str(80):
                    path=19
                elif str(path)<str(70) and str(path)>=str(60):
                    path=16
                elif str(path)<str(60) and str(path)>=str(50):
                    path=13
                elif str(path)<str(50) and str(path)>=str(40):
                    path=10
                elif str(path)<str(40) and str(path)>=str(30):
                    path=7
                elif str(path)<str(30) and str(path)>=str(20):
                    path=4
                else:
                    path=0
                rating.append(path)
            df['rate3']=rating

        def sum2():
            num1=df['rate'] #별점
            num2=df['rate2'] #별점 준 사람 수
            num3=df['rate3'] #블로그 리뷰
            num4=df['rate4'] #거리

            sums=num1+num2+num3+num4
            sums=np.array(sums)
            df['sums']=sums
            sums.sort()
        
            return sums

        def blog_km_sum():                      
            num3=df['rate3'] #블로그 리뷰
            num4=df['rate4'] #거리

            blog_km=num3+num4
            blog_km=np.array(blog_km)
            df['blog_km']=blog_km
            blog_km.sort()

            return blog_km

        def km_star_sum():
            num1=df['rate'] #별점
            num4=df['rate4'] #블로그 리뷰
            
            km_star=num1+num4
            km_star=np.array(km_star)
            df['km_star']=km_star
            km_star.sort()

            return km_star

        def blog_star_sum():
            num1=df['rate'] #별점
            num3=df['rate3'] #블로그 리뷰
            
            blog_star=num1+num3
            blog_star=np.array(blog_star)
            df['blog_star']=blog_star
            blog_star.sort()

            return blog_star
            
        def km_star_blog_sum():
            num1=df['rate'] #별점
            num3=df['rate3'] #블로그 리뷰
            num4=df['rate4'] #거리
            
            km_star_blog=num1+num3+num4
            km_star_blog=np.array(km_star_blog)
            df['km_star_blog']=km_star_blog
            km_star_blog.sort()

            return km_star_blog

        def top100(value):
            value=np.array(value)
            value.sort()
            value=value[::-1]
            top100=value[100]

            return top100

        def df_top100(top100):
            result=[]
            result2=[]
            result3=[]
            result4=[]
            result5=[]
            result6=[]
            result7=[]
            result8=[]

            df2=pd.DataFrame(columns=['사업장명','위도','경도','kakao_star','kakao_star_nums','kakao_blog_review'])
            for i in range(len(df)):
                if sums[i]>=top100:
                    result.append(df.loc[i]['사업장명'])
                    result2.append(df.loc[i]['위도'])
                    result3.append(df.loc[i]['경도'])
                    result4.append(df.loc[i]['kakao_star'])
                    result5.append(df.loc[i]['kakao_star_nums'])
                    result6.append(df.loc[i]['kakao_blog_review'])
                    result7.append(df.loc[i]['sums']) 
                    result8.append(df.loc[i]['distance'])            
            df2['사업장명']=result
            df2['위도']=result2
            df2['경도']=result3
            df2['kakao_star']=result4
            df2['kakao_star_nums']=result5
            df2['kakao_blog_review']=result6
            df2['sums']=result7
            df2['distance']=result8
            return df2
        
        def df_top103(top100):
            result=[]
            result2=[]
            result3=[]
            result4=[]
            result5=[]
            result6=[]
            result7=[]
            result8=[]
            result9=[]
            result10=[]
            result11=[]
            result12=[]
            df3=pd.DataFrame(columns=['사업장명','위도','경도','kakao_star','kakao_star_nums','kakao_blog_review','blog_km','km_star','blog_star','km_star_blog'])
            for i in range(len(df)):
                if blog_km[i]>=top103:
                    result.append(df.loc[i]['사업장명'])
                    result2.append(df.loc[i]['위도'])
                    result3.append(df.loc[i]['경도'])
                    result4.append(df.loc[i]['kakao_star'])
                    result5.append(df.loc[i]['kakao_star_nums'])
                    result6.append(df.loc[i]['kakao_blog_review'])
                    result7.append(df.loc[i]['sums']) 
                    result8.append(df.loc[i]['distance'])
                    result9.append(df.loc[i]['blog_km'])
                    result10.append(df.loc[i]['km_star'])
                    result11.append(df.loc[i]['blog_star'])
                    result12.append(df.loc[i]['km_star_blog'])
            df3['사업장명']=result
            df3['위도']=result2
            df3['경도']=result3
            df3['kakao_star']=result4
            df3['kakao_star_nums']=result5
            df3['kakao_blog_review']=result6
            df3['sums']=result7
            df3['distance']=result8
            df3['blog_km']=result9
            df3['km_star']=result10
            df3['blog_star']=result11
            df3['km_star_blog']=result12
            return df3
        def df_top104(top100):
            result=[]
            result2=[]
            result3=[]
            result4=[]
            result5=[]
            result6=[]
            result7=[]
            result8=[]
            result9=[]
            result10=[]
            result11=[]
            result12=[]
            df4=pd.DataFrame(columns=['사업장명','위도','경도','kakao_star','kakao_star_nums','kakao_blog_review','blog_km','km_star','blog_star','km_star_blog'])
            for i in range(len(df)):
                if km_star[i]>=top104:
                    result.append(df.loc[i]['사업장명'])
                    result2.append(df.loc[i]['위도'])
                    result3.append(df.loc[i]['경도'])
                    result4.append(df.loc[i]['kakao_star'])
                    result5.append(df.loc[i]['kakao_star_nums'])
                    result6.append(df.loc[i]['kakao_blog_review'])
                    result7.append(df.loc[i]['sums']) 
                    result8.append(df.loc[i]['distance'])
                    result9.append(df.loc[i]['blog_km'])
                    result10.append(df.loc[i]['km_star'])
                    result11.append(df.loc[i]['blog_star'])
                    result12.append(df.loc[i]['km_star_blog'])
            df4['사업장명']=result
            df4['위도']=result2
            df4['경도']=result3
            df4['kakao_star']=result4
            df4['kakao_star_nums']=result5
            df4['kakao_blog_review']=result6
            df4['sums']=result7
            df4['distance']=result8
            df4['blog_km']=result9
            df4['km_star']=result10
            df4['blog_star']=result11
            df4['km_star_blog']=result12
            return df4

        def df_top105(top100):
            result=[]
            result2=[]
            result3=[]
            result4=[]
            result5=[]
            result6=[]
            result7=[]
            result8=[]
            result9=[]
            result10=[]
            result11=[]
            result12=[]
            df5=pd.DataFrame(columns=['사업장명','위도','경도','kakao_star','kakao_star_nums','kakao_blog_review','blog_km','km_star','blog_star','km_star_blog'])
            for i in range(len(df)):
                if blog_star[i]>=top105:
                    result.append(df.loc[i]['사업장명'])
                    result2.append(df.loc[i]['위도'])
                    result3.append(df.loc[i]['경도'])
                    result4.append(df.loc[i]['kakao_star'])
                    result5.append(df.loc[i]['kakao_star_nums'])
                    result6.append(df.loc[i]['kakao_blog_review'])
                    result7.append(df.loc[i]['sums']) 
                    result8.append(df.loc[i]['distance'])
                    result9.append(df.loc[i]['blog_km'])
                    result10.append(df.loc[i]['km_star'])
                    result11.append(df.loc[i]['blog_star'])
                    result12.append(df.loc[i]['km_star_blog'])
            df5['사업장명']=result
            df5['위도']=result2
            df5['경도']=result3
            df5['kakao_star']=result4
            df5['kakao_star_nums']=result5
            df5['kakao_blog_review']=result6
            df5['sums']=result7
            df5['distance']=result8
            df5['blog_km']=result9
            df5['km_star']=result10
            df5['blog_star']=result11
            df5['km_star_blog']=result12
            return df5

        def df_top106(top100):
            result=[]
            result2=[]
            result3=[]
            result4=[]
            result5=[]
            result6=[]
            result7=[]
            result8=[]
            result9=[]
            result10=[]
            result11=[]
            result12=[]
            df6=pd.DataFrame(columns=['사업장명','위도','경도','kakao_star','kakao_star_nums','kakao_blog_review','blog_km','km_star','blog_star','km_star_blog'])
            for i in range(len(df)):
                if km_star_blog[i]>=top106:
                    result.append(df.loc[i]['사업장명'])
                    result2.append(df.loc[i]['위도'])
                    result3.append(df.loc[i]['경도'])
                    result4.append(df.loc[i]['kakao_star'])
                    result5.append(df.loc[i]['kakao_star_nums'])
                    result6.append(df.loc[i]['kakao_blog_review'])
                    result7.append(df.loc[i]['sums']) 
                    result8.append(df.loc[i]['distance'])
                    result9.append(df.loc[i]['blog_km'])
                    result10.append(df.loc[i]['km_star'])
                    result11.append(df.loc[i]['blog_star'])
                    result12.append(df.loc[i]['km_star_blog'])
            df6['사업장명']=result
            df6['위도']=result2
            df6['경도']=result3
            df6['kakao_star']=result4
            df6['kakao_star_nums']=result5
            df6['kakao_blog_review']=result6
            df6['sums']=result7
            df6['distance']=result8
            df6['blog_km']=result9
            df6['km_star']=result10
            df6['blog_star']=result11
            df6['km_star_blog']=result12
            return df6
        
        def dis():
            cc = []
            tv = []
            rating=[]
            rating2=[]
            for i in range(len(df)):
                cc.append(df.iloc[i, 3]) #위도
                tv.append(df.iloc[i, 4]) #경도

            for i in range(len(df)):
                #Latitude, Longitude
                c = cc[i],tv[i]
                rating2.append(haversine(Place, c, unit = 'km'))
                
            df['distance']=rating2
            for path in df['distance']:
                if path<1:
                    path=25
                elif path>=1 and path<2:
                    path=22
                elif path>=2 and path<3:
                    path=19
                elif path>=4 and path<5:
                    path=16
                elif path>=5 and path<6:
                    path=13
                elif path>=6 and path<7:
                    path=10
                elif path>=7 and path<8:
                    path=7
                elif path>=8 and path<9:
                    path=3
                elif path>=9 and path<10:
                    path=1
                else:
                    path=0
                rating.append(path)
            df['rate4']=rating

        def maps(list,values):
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df2)):
                iframe = folium.IFrame(str(df2.loc[i]['사업장명']) +
                                                "<br><b>별점 : </b>"+str(df2.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                str(df2.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df2.loc[i]['kakao_blog_review']))
                popup = folium.Popup(iframe,
                                    min_width=200,
                                    max_width=200)
                marker01=folium.Marker([df2.loc[i]['위도'], df2.loc[i]['경도']],
                                                popup = popup,icon=folium.Icon(color = 'lightgray'))
                marker01.add_to(m)
                marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
            data = io.BytesIO()
            m.save(data, close_file=False)
            return data

        def df2_sums():
            num1=df2['kakao_blog_review']
            num1=np.array(num1)
            num1.sort()
            num1=num1[::-1]
            try:
                return num1[10]
            except:
                return num1

        def df2_dissum():
            num2=df2['distance']
            num2=np.array(num2)
            num2.sort()
            try:
                return num2[10]
            except:
                return num2
        
        def df2_starsum():
            num3=df2['kakao_star']
            num3=np.array(num3)
            num3.sort()
            num3=num3[::-1]
            try:
                return num3[10]
            except:
                return num3

        def df2_blogkmsum():
            num4=df3['blog_km']
            num4=np.array(num4)
            num4.sort()
            num4=num4[::-1]
           
            try:
                return num4[10]
            except:
                return num4
        def df2_kmstarsum():
            num5=df4['km_star']
            num5=np.array(num5)
            num5.sort()
            num5=num5[::-1]
            try:
                return num5[10]
            except:
                return num5
        def df2_blogstarsum():
            num6=df5['blog_star']
            num6=np.array(num6)
            num6.sort()
            num6=num6[::-1]
           
            try:
                return num6[10]
            except:
                return num6

        def df2_kmstarblogsum():
            num7=df6['km_star_blog']
            num7=np.array(num7)
            num7.sort()
            num7=num7[::-1]
           
            try:
                return num7[10]
            except:
                return num7
            

        global df2,df3,df4,df5,df6
        global num1,num2,num3,num4,num5,num6,num7
        global statenum

        global cb_1
        global cb_2
        global cb_3

        global top102
        global top103
        global top104
        global top105
        global top106

        global blog_km
        global km_star
        global blog_star
        global km_star_blog

        try:
            dataset.iloc[0][{s}]= dataset.iloc[0][{s}]+1
        except:
            pass
        dataset.to_csv(f'./csv\\음식점카운트.csv',sep=',',encoding='cp949',index=False)
    
        data=select()
        s2=data[1]
        s3=data[0]
        csv_select2=f'./csv\\{s2}.csv'
        try:
            df10 =  pd.read_csv(csv_select2, encoding='cp949')
        except:
            df10 =  pd.read_csv(csv_select2, encoding='utf-8')
        csv_select3=f'./csv\\{s3}.csv'
        try:
            df11 =  pd.read_csv(csv_select3, encoding='cp949')
        except:
            df11 =  pd.read_csv(csv_select3, encoding='utf-8')
        df12=pd.concat([df10, df11])
        df12.to_csv('./csv\\추천지도.csv',sep=',',encoding='cp949',index=False)

        csv_select=f'./csv\\{s}.csv'
        try:
            df =  pd.read_csv(csv_select, encoding='cp949')
        except:
            df =  pd.read_csv(csv_select, encoding='utf-8')
       
        star_rate(df)
        star_nums(df)
        kakao_blog_review(df)
        dis()

        blog_km=blog_km_sum()
        km_star=km_star_sum()
        blog_star=blog_star_sum()
        km_star_blog=km_star_blog_sum()
        sums=sum2()

        top102=top100(sums)
        top103=top100(blog_km)
        top104=top100(km_star)
        top105=top100(blog_star)
        top106=top100(km_star_blog)
        
        df2=df_top100(top102)
        df3=df_top103(top103)
        df4=df_top104(top104)
        df5=df_top105(top105)
        df6=df_top106(top106)

        num1=df2_sums()
        num2=df2_dissum()
        num3=df2_starsum()
        num4=df2_blogkmsum() #리뷰+거리
        num5=df2_kmstarsum() #거리+별점
        num6=df2_blogstarsum() #리뷰+별점
        num7=df2_kmstarblogsum() #전부다
        
        maps2=maps(sums,top102)
        self.setHtml(maps2.getvalue().decode())
        self.resize(1100, 900)


        btn_main = QPushButton(self)
        btn_main.setGeometry(QtCore.QRect(20, 860, 50, 23))
        btn_main.setText('Home')
        btn_main.clicked.connect(self.show_main_window)
        btn_main.setStyleSheet("background-color: rgba(255, 255, 255, 230);\n"
"gridline-color: rgba(255, 255, 255, 150);\n"
"border-width: 2px;\n"
"border-radius: 30px;\n"
"border-style: solid;\n"
"border-color: rgba(85, 170, 127,100);\n"
"font: 75 11pt \"KoPub돋움체 Medium\";\n"
"color: rgb(65, 65, 65);\n"
"")     

        frame = QLabel(self)
        frame.setGeometry(QtCore.QRect(880, 0, 220, 900))
        frame.setStyleSheet("background-color: rgba(235, 235, 235, 225);\n"
"gridline-color: rgb(33, 33, 33);\n"
"border-radius: 32px;\n"
"border-style: solid;\n"
"border-color: rgb(85, 85, 127);\n"
"")     
        global frame_2
        frame_2 = QTextBrowser(self) #리스트 출력할곳
        frame_2.setGeometry(QtCore.QRect(880, 400, 211, 491))
        frame_2.setObjectName("list")
        frame_2.setStyleSheet("background-color: rgba(85, 170, 255, 15);\n"
"font: 75 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(65, 65, 65);\n"
"gridline-color: rgb(33, 33, 33);\n"
"border-radius: 25px;\n"
"border-style: ridge;\n"
"border-color: rgb(85, 85, 127);\n"
"")   
        
        frame_3 = QWidget(self)
        frame_3.setGeometry(QtCore.QRect(880, 110, 221, 231))
        frame_3.setObjectName("verticalLayoutWidget")
        verticalLayout = QVBoxLayout(frame_3)
        verticalLayout.setContentsMargins(12, 0, 0, 20)
        verticalLayout.setObjectName("verticalLayout")

        cb_1 = QCheckBox('리뷰',frame_3)
        cb_1.setStyleSheet("\n"
"font: 75 13pt \"KoPub돋움체 Medium\";\n"
"color: rgb(65, 65, 65);\n"
"")
        cb_1.setObjectName("cb_1")
        cb_1.stateChanged.connect(self.review4)
        cb_1.stateChanged.connect(self.show_review)
        verticalLayout.addWidget(cb_1)

        cb_2 = QCheckBox('거리',frame_3)
        cb_2.setStyleSheet("\n"
"font: 75 13pt \"KoPub돋움체 Medium\";\n"
"color: rgb(65, 65, 65);\n"
"")
        cb_2.setObjectName("cb_2")
        cb_2.stateChanged.connect(self.review4)
        cb_2.stateChanged.connect(self.show_review)
        verticalLayout.addWidget(cb_2)

        cb_3 = QCheckBox('별점',frame_3)
        cb_3.setStyleSheet("\n"
"font: 75 13pt \"KoPub돋움체 Medium\";\n"
"color: rgb(65, 65, 65);\n"
"")
        cb_3.setObjectName("cb_3")
        cb_3.stateChanged.connect(self.review4)
        cb_3.stateChanged.connect(self.show_review)
        verticalLayout.addWidget(cb_3)
        
        frame_4 = QLabel(self)
        frame_4.setGeometry(QtCore.QRect(900, 350, 101, 51))
        frame_4.setStyleSheet("\n"
"font: 75 16pt \"KoPub돋움체 Medium\";\n"
"color: rgb(65, 65, 65);\n"
"\n"
"border-radius: 20px;\n"
"") 
        frame_4.setText("리스트")
        
        for i in range(len(df2)):
            frame_2.append(str(df2.loc[i]['사업장명'])+'\n')
    
        self.show()
    
    def show_main_window(self):
        self.close()
        self.parent.set_content("Main")

    def show_review(self,):
        if cb_1.isChecked()==True and cb_2.isChecked()==False and cb_3.isChecked()==False: #리뷰만
            frame_2.clear()
            for i in range(len(df2)):
                if df2.iloc[i]['kakao_blog_review']>=num1:
                    frame_2.append(str(df2.loc[i]['사업장명']))
                    frame_2.append('리뷰:'+str(df2.loc[i]['kakao_blog_review'])+'개'+'\n')
        
        if cb_2.isChecked()==True and cb_1.isChecked()==False and cb_3.isChecked()==False: #거리만
            frame_2.clear()
            for i in range(len(df2)):
                if df2.iloc[i]['distance']<num2:
                    frame_2.append(str(df2.loc[i]['사업장명']))
                    frame_2.append('거리:'+str(round(df2.loc[i]['distance'],1))+'km'+'\n')

        if cb_3.isChecked()==True and cb_1.isChecked()==False and cb_2.isChecked()==False: #별점만
            frame_2.clear()
            for i in range(len(df2)):
                if df2.iloc[i]['kakao_star']>=num3:
                    frame_2.append(str(df2.loc[i]['사업장명']))
                    frame_2.append('별점:'+str(df2.loc[i]['kakao_star'])+'★'+'\n')

        if  cb_1.isChecked()==True and cb_2.isChecked()==True and cb_3.isChecked()==False:  #리뷰+거리
            frame_2.clear()
            for i in range(len(df3)):
                if df3.iloc[i]['blog_km']>=num4:
                    frame_2.append(str(df3.loc[i]['사업장명']))
                    frame_2.append('리뷰:'+str(df3.loc[i]['kakao_blog_review'])+'개')
                    frame_2.append('거리:'+str(round(df3.loc[i]['distance'],1))+'km'+'\n')

        if  cb_1.isChecked()==True and cb_3.isChecked()==True and cb_2.isChecked()==False:  #리뷰+별점
            frame_2.clear()
            for i in range(len(df4)):
                if df4.iloc[i]['km_star']>=num5:
                    frame_2.append(str(df4.loc[i]['사업장명']))
                    frame_2.append('리뷰:'+str(df4.loc[i]['kakao_blog_review'])+'개')
                    frame_2.append('별점:'+str(df4.loc[i]['kakao_star'])+'★'+'\n')

        if  cb_2.isChecked()==True and cb_3.isChecked()==True and cb_1.isChecked()==False:  #거리+별점
            frame_2.clear()
            for i in range(len(df5)):
                if df5.iloc[i]['blog_star']>=num6:
                    frame_2.append(str(df5.loc[i]['사업장명']))
                    frame_2.append('거리:'+str(round(df5.loc[i]['distance'],1))+'km')
                    frame_2.append('별점:'+str(df5.loc[i]['kakao_star'])+'★'+'\n')
        
        if  cb_1.isChecked()==True and cb_2.isChecked()==True and cb_3.isChecked()==True:   #리뷰+거리+별점
            frame_2.clear()
            for i in range(len(df6)):
                if df6.iloc[i]['km_star_blog']>=num7:
                    frame_2.append(str(df6.loc[i]['사업장명']))
                    frame_2.append('리뷰:'+str(df6.loc[i]['kakao_blog_review'])+'개')
                    frame_2.append('거리:'+str(round(df6.loc[i]['distance'],1))+'km'+'\n')
                    frame_2.append('별점:'+str(df6.loc[i]['kakao_star'])+'★'+'\n')

        if  cb_1.isChecked()==False and cb_2.isChecked()==False and cb_3.isChecked()==False:
            frame_2.clear()
            for i in range(len(df2)):
                frame_2.append(str(df2.loc[i]['사업장명']))
    
    def review4(self, state):
        if cb_1.isChecked()==True and cb_2.isChecked()==False and cb_3.isChecked()==False: #리뷰만
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df2)):
                if df2.iloc[i]['kakao_blog_review']>=num1:                    
                    iframe = folium.IFrame(str(df2.loc[i]['사업장명']) +
                                                    "<br><b>별점 : </b>"+str(df2.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                    str(df2.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df2.loc[i]['kakao_blog_review']))
                    popup = folium.Popup(iframe,
                                        min_width=200,
                                        max_width=200)
                    marker01=folium.Marker([df2.loc[i]['위도'], df2.loc[i]['경도']],
                                                    popup = popup,icon=folium.Icon(color = 'red'))
                    marker01.add_to(m)
                    marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                    marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
                data = io.BytesIO()
                m.save(data, close_file=False)
                self.setHtml(data.getvalue().decode())
                self.resize(1100, 900)
                self.show()

        if cb_1.isChecked()==False and cb_2.isChecked()==True and cb_3.isChecked()==False: #거리만
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df2)):
                if df2.iloc[i]['distance']<num2:                    
                    iframe = folium.IFrame(str(df2.loc[i]['사업장명']) +
                                                    "<br><b>별점 : </b>"+str(df2.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                    str(df2.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df2.loc[i]['kakao_blog_review']))
                    popup = folium.Popup(iframe,
                                        min_width=200,
                                        max_width=200)
                    marker01=folium.Marker([df2.loc[i]['위도'], df2.loc[i]['경도']],
                                                    popup = popup,icon=folium.Icon(color = 'blue'))
                    marker01.add_to(m)
                    marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                    marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
                data = io.BytesIO()
                m.save(data, close_file=False)
                self.setHtml(data.getvalue().decode())
                self.resize(1100, 900)
                self.show()

        if cb_1.isChecked()==False and cb_2.isChecked()==False and cb_3.isChecked()==True: #별점만
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df2)):
                if df2.iloc[i]['kakao_star']>=num3:                    
                    iframe = folium.IFrame(str(df2.loc[i]['사업장명'])+
                                                    "<br><b>별점 : </b>"+str(df2.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                    str(df2.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df2.loc[i]['kakao_blog_review']))
                    popup = folium.Popup(iframe,
                                        min_width=200,
                                        max_width=200)
                    marker01=folium.Marker([df2.loc[i]['위도'], df2.loc[i]['경도']],
                                                    popup = popup,icon=folium.Icon(color = 'orange'))
                    marker01.add_to(m)
                    marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                    marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
                data = io.BytesIO()
                m.save(data, close_file=False)
                self.setHtml(data.getvalue().decode())
                self.resize(1100, 900)
                self.show()
        
        
        if  cb_1.isChecked()==True and cb_2.isChecked()==True and cb_3.isChecked()==False:  #리뷰+거리
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df3)):
                if df3.iloc[i]['blog_km']>=num4:                    
                    iframe = folium.IFrame(str(df3.loc[i]['사업장명']) +
                                                    "<br><b>별점 : </b>"+str(df3.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                    str(df3.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df3.loc[i]['kakao_blog_review']))
                    popup = folium.Popup(iframe,
                                        min_width=200,
                                        max_width=200)
                    marker01=folium.Marker([df3.loc[i]['위도'], df3.loc[i]['경도']],
                                                    popup = popup,icon=folium.Icon(color = 'purple'))
                    marker01.add_to(m)
                    marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                    marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
                data = io.BytesIO()
                m.save(data, close_file=False)
                self.setHtml(data.getvalue().decode())
                self.resize(1100, 900)
                self.show()

        
        if  cb_1.isChecked()==False and cb_2.isChecked()==True and cb_3.isChecked()==True:  #거리+별점  num5=df2_kmstarsum() #거리+별점
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df4)):
                if df4.iloc[i]['km_star']>=num5:                    
                    iframe = folium.IFrame(str(df4.loc[i]['사업장명']) +
                                                    "<br><b>별점 : </b>"+str(df4.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                    str(df4.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df4.loc[i]['kakao_blog_review']))
                    popup = folium.Popup(iframe,
                                        min_width=200,
                                        max_width=200)
                    marker01=folium.Marker([df4.loc[i]['위도'], df4.loc[i]['경도']],
                                                    popup = popup,icon=folium.Icon(color = 'green'))
                    marker01.add_to(m)
                    marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                    marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
                data = io.BytesIO()
                m.save(data, close_file=False)
                self.setHtml(data.getvalue().decode())
                self.resize(1100, 900)
                self.show()
        if  cb_1.isChecked()==True and cb_2.isChecked()==False and cb_3.isChecked()==True:  #리뷰+별점
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df5)):
                if df5.iloc[i]['blog_star']>=num6:                    
                    iframe = folium.IFrame(str(df5.loc[i]['사업장명']) +
                                                    "<br><b>별점 : </b>"+str(df5.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                    str(df5.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df5.loc[i]['kakao_blog_review']))
                    popup = folium.Popup(iframe,
                                        min_width=200,
                                        max_width=200)
                    marker01=folium.Marker([df5.loc[i]['위도'], df5.loc[i]['경도']],
                                                    popup = popup,icon=folium.Icon(color = 'lightblue'))
                    marker01.add_to(m)
                    marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                    marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
                data = io.BytesIO()
                m.save(data, close_file=False)
                self.setHtml(data.getvalue().decode())
                self.resize(1100, 900)
                self.show()
        if  cb_1.isChecked()==True and cb_2.isChecked()==True and cb_3.isChecked()==True:   #리뷰+거리+별점
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df6)):
                if df6.iloc[i]['km_star_blog']>=num7:                    
                    iframe = folium.IFrame(str(df6.loc[i]['사업장명']) +
                                                    "<br><b>별점 : </b>"+str(df6.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                    str(df6.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df6.loc[i]['kakao_blog_review']))
                    popup = folium.Popup(iframe,
                                        min_width=200,
                                        max_width=200)
                    marker01=folium.Marker([df6.loc[i]['위도'], df6.loc[i]['경도']],
                                                    popup = popup,icon=folium.Icon(icon='star',color = 'beige'))
                    marker01.add_to(m)
                    marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                    marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
                data = io.BytesIO()
                m.save(data, close_file=False)
                self.setHtml(data.getvalue().decode())
                self.resize(1100, 900)
                self.show()
        
        if cb_1.isChecked()==False and cb_2.isChecked()==False and cb_3.isChecked()==False: #체크X
            m = folium.Map(
                location=Place, tiles='Stamen Terrain', zoom_start=13
            )
            for i in range(len(df2)):
                iframe = folium.IFrame(str(df2.loc[i]['사업장명']) +
                                                "<br><b>별점 : </b>"+str(df2.loc[i]['kakao_star'])+"<br><b>별점리뷰 수: </b>"+
                                                str(df2.loc[i]['kakao_star_nums'])+"<br><b>블로그리뷰 수: </b>"+str(df2.loc[i]['kakao_blog_review']))
                popup = folium.Popup(iframe,
                                    min_width=200,
                                    max_width=200)
                marker01=folium.Marker([df2.loc[i]['위도'], df2.loc[i]['경도']],
                                                popup = popup,icon=folium.Icon(color = 'lightgray'))
                marker01.add_to(m)
                marker02=folium.Marker(Place, number_of_sides=8, icon=folium.Icon(color = 'green'), popup='현재위치').add_to(m)
                marker02=folium.CircleMarker(Place, number_of_sides=8,radius=270 ).add_to(m)
            data = io.BytesIO()
            m.save(data, close_file=False)
            self.setHtml(data.getvalue().decode())
            self.resize(1100, 900)
            self.show()

    def show_main_window(self):
        self.close()
        self.parent.set_content("Main")
    
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.set_content("Main")
    def set_content(self, new_content):
        w = QtWebEngineWidgets.QWebEngineView()
        if new_content == "Main":
            self.content = MainWidget(self)
        elif new_content == "choice1":           
            self.content = choice1widget(self)
        elif new_content == "choice2":
            self.content = choice2widget(self)
        elif new_content == "choice3":
            self.content = choice3widget(self)
        elif new_content == "check2":
            self.content = check2widget(self)
        elif new_content == "check":
            self.content = checkwidget(self)
       
app = QtWidgets.QApplication([])
main = MainWindow()
app.exec()