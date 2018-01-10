
# -*- coding: utf-8 -*-

#######################################
#                                                                                                   #
#   This RASPBERRY PI  is node( 1 ) of STAMPRALLY    #
#                                                                                                   #
#######################################

import pygame
from pygame.locals import *
import datetime
import time
import RPi.GPIO as GPIO
import codecs

import sys
file_path='/home/pi/Desktop/import/'
sys.path.append('/usr/local/src/nfcpy')
sys.path.append('/home/pi/.local/lib/python2.7/site-packages')
import nfc
import readICCard
import random
import requests
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


#-----------------------------------------------------------------------------------------#
# ウィンドウ画面の宣言 #
#
# 画面遷移するPygameのウィンドウの初期化

pygame.init()
screen = pygame.display.set_mode((800, 480)) #ウィンドウサイズ 800x400
pygame.display.set_caption("Stamp_Rally") #ウィンドウの名前
questionnum = "2" #ウィンドウの数


#-----------------------------------------------------------------------------------------#
# 関数 - テキストファイル読み込み #
#
# 同じディレクトリにあるテキストファイル名を引数に取り、1行ずつリストに入れて返す.
# 引数: ファイルの名前 , 返り値: 文字列1行ずつのリスト.

def tripp(listname):
    global li
    li = []
    for line in codecs.open(listname, 'r', 'utf_8'):
        li.append(line.rstrip('\r\n'))      
    return li


#-----------------------------------------------------------------------------------------#
# pin #
#
# タクトスイッチと繋がっているピンの宣言.
# 現在では22, 23, 24番目を使用している.

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) #RED
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP) #BLUE
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP) #GREEN

#-----------------------------------------------------------------------------------------#
# countdown & answer #
#
# クイズに回答したときのカウントダウンに使う画像とフォントの宣言.

cnt3 = pygame.image.load(file_path + "s_33.gif").convert()
cnt2 = pygame.image.load(file_path + "s_22.gif").convert()
cnt1 = pygame.image.load(file_path + "s_11.gif").convert()
OK = pygame.image.load(file_path + "OK.png").convert()
NG = pygame.image.load(file_path + "NG.png").convert()
stamp = pygame.image.load(file_path + "s_stamp_rally.png").convert()
myfont1 = pygame.font.Font(file_path + "ipaexg.ttf", 56)

#-----------------------------------------------------------------------------------------#
# iccard top page #
#
# ICカード読み取り中のトップ画面に必要なメッセージと画像の宣言.
# tripp(ファイルパス + ファイル名)で1行ずつ読み取り, for文でicmesseのリストにpygameの文字として格納.
# icmesseposでそれぞれの位置を指定しておき, 後で呼び出すときに簡略化.

tripp(file_path + "pleaseICCard.txt")
myfont2 = pygame.font.Font(file_path + "ipaexg.ttf", 50)

icmesse = []
for messa in range(len(li)):
    icmesse.append(myfont2.render(li[messa], True, (0,0,0)))

icmessepos = [[30, 20], [260, 90], [30, 270], [40, 350]]

#-----------------------------------------------------------------------------------------#
# not registered # -> reqreg
#
# マスターにICカードが登録されていないときの画面のメッセージと画像の宣言.
# 前述の方法と同じようにリストを作成している.
# pngの画像は hanko = ... で読み取り, colorkey, name.set_colorkeyで透過処理をしている.
# 素材が「いらすとや」のものであるためこの手順を使用.

tripp(file_path + "pleaseRegister.txt")

plsreg = []
for messa in range(len(li)):
    plsreg.append(myfont2.render(li[messa], True, (0,0,0)))

hanko = pygame.image.load(file_path + "hanko_maruin.png").convert()
colorkey = hanko.get_at((0,0))
hanko.set_colorkey(colorkey, RLEACCEL)

plsregpos = [[20, 20], [20, 100], [40, 160]]

#-----------------------------------------------------------------------------------------#
# already solved # -> alsolve
#
# 同じノード(端末)で回答済み(スタンプ獲得済み)の場合の画面の宣言
# 以下略

tripp(file_path + "alreadysolved.txt")

alsol = []
for messa in range(len(li)):
    alsol.append(myfont2.render(li[messa], True, (0,0,0)))

taihen = pygame.image.load(file_path + "hanko_taihenyokudekimashita.png").convert()
colorkey = taihen.get_at((0,0))
taihen.set_colorkey(colorkey, RLEACCEL)
"""
find = pygame.image.load(file_path + "pose_sagasu_kyorokyoro_man.png").convert()
colorkey = find.get_at((0,0))
find.set_colorkey(colorkey, RLEACCEL)
"""

alsolpos = [[30, 50], [30, 120], [30, 230]]

#-----------------------------------------------------------------------------------------#
# gettedpoint #
#
# 最後に表示されるスタンプ獲得数が確認できる画面の宣言

gfont1 = pygame.font.Font(file_path + "ipaexg.ttf", 56)
gfont2 = pygame.font.Font(file_path + "ipaexg.ttf", 80)
gfont3 = pygame.font.Font(file_path + "ipaexg.ttf", 45)

getmesse = []
getmesse.append(gfont1.render(u"現在", True, (0,0,0)))
getmesse.append(gfont2.render(u"/", True, (0,0,0)))
getmesse.append(gfont2.render(questionnum, True, (0,0,0)))
getmesse.append(gfont1.render(u"スタンプ", True, (0,0,0)))
getmesse.append(gfont1.render(u"獲得済みです！", True, (0,0,0)))

getmessepos = [[30,20], [250, 40], [290, 60], [400, 20], [400, 90], [200, 20], [30, 260], [30, 340]]


#-----------------------------------------------------------------------------------------#
# question no.1 #
#
# 1問目のクイズの宣言

tripp(file_path + "question1.txt")
qfont = pygame.font.Font(file_path + "ipaexg.ttf", 26)

qms1 = []
for messa in range(len(li)):
    qms1.append(qfont.render(li[messa], True, (0,0,0)))

qms1pos = [[20, 30], [20, 75], [40, 140], [40, 185], [10, 265], [10, 315], [10, 365]]

#-----------------------------------------------------------------------------------------#
# question No.2 #
#
# 2問目

tripp(file_path + "question2.txt")

qms2 = []
for messa in range(len(li)):
    qms2.append(qfont.render(li[messa], True, (0,0,0)))

robot = pygame.image.load(file_path + "omocha_robot.png").convert()
colorkey = robot.get_at((0,0))
robot .set_colorkey(colorkey, RLEACCEL)

qms2pos = [[20, 30], [20, 75], [20, 120], [20, 165], [20, 210], [20, 255]]
robotpos = [[20, 310], [420, 310], [220, 310]]

#-----------------------------------------------------------------------------------------#
# question No.3 #
#
# 3問目

tripp(file_path + "question3.txt")

qms3 = []
for messa in range(len(li)):
    qms3.append(qfont.render(li[messa], True, (0,0,0)))

milk = pygame.image.load(file_path + "milk_bin.png").convert()
milky = pygame.transform.scale(milk, (345/2 , 400/2))
colorkey = milky.get_at((0,0))
milky.set_colorkey(colorkey, RLEACCEL)
bmushi = pygame.image.load(file_path + "mushiba_boy.png").convert()
mushiba = pygame.transform.scale(bmushi, (339/2 , 400/2))
colorkey = mushiba.get_at((0,0))
mushiba.set_colorkey(colorkey, RLEACCEL)

qms3pos = [[20, 30], [20, 75],  [20, 120], [40, 180], [40, 225], [30, 290], [30, 335], [30, 380]]

#-----------------------------------------------------------------------------------------#



#-----------------------------------------------------------------------------------------#
# 関数 - カウントダウンと正解不正解判定 #
#
# counting(3~1)でカウントダウン画面を表示.
# 引数 ans が 0 の場合 = 正解, 1の場合 = はずれとなっている.
# その後 Result関数へ

def CountDown(ans):
    counting(cnt3)
    counting(cnt2)
    counting(cnt1)
    if ans == 0:
        Result(OK,  0)
    else:
        Result(NG,  1)

#-----------------------------------------------------------------------------------------#
# 関数 - カウントダウン #
#
# 1秒で終わる. 3 -> 2 -> 1 を表現したくて作った.

def counting(filename):
    start = time.time() 
    while True:
        end = time.time() - start
        screen.fill((255,255,255))
        screen.blit(filename, (240,70))
        pygame.display.update()
        if end >= 1:
            print("counting")
            break


#-----------------------------------------------------------------------------------------#
# 関数 - 正解かはずれかの結果画面 #
#
# 引数 filename( OK or NG )とx( 0 or 1)を取る.
# x = 0の正解の時はサーバにポイント1追加のURLで,
# x = 1のはずれの時はポイント0追加のURLでセッション通信する.
# 3秒後にポイント確認画面へ移る.


def Result(filename,  x):
    start = time.time()
    session = requests.session()
    
    if x == 0:
        URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/register.php?node=1&point=1&IDm="
        totalURL = URL + ID
        session.get(totalURL)

    else:
        URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/register.php?node=1&point=0&IDm="
        totalURL = URL + ID
        session.get(totalURL)
     
    while True:
        end = time.time() - start
        if end >= 3:         
            gettedPoint(x)
            
        screen.fill((255,255,255))
        screen.blit(filename, (60,30))
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == QUIT:       
                pygame.quit()       
                sys.exit()

#-----------------------------------------------------------------------------------------#
# 関数 - 獲得済みポイント確認画面 #
#
# サーバのホームページに入り, 何ポイントかとれているか確認する.
# textで無理やりポイント数を取ってきている. -> getpoint
# ポイント数が問題数と同数以上(全問正解)の場合 -> 景品交換可能のメッセージ,
# ポイント数が問題数以下であり, 正解した場合 -> 他のスタンプを探そうメッセ―ジ,
# ポイント数が問題数以下であり, 不正解の場合 -> もう1回解いてみようメッセージがでるようになっている.
# またこれらの分岐によって四角形の色が変わるようにしている.
# for文でリストに入れたメッセージを設置していっている.

def gettedPoint(ans):
    start = time.time()
    session = requests.session()
    URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/master.php?IDm="
    totalURL = URL + ID
    check = session.get(totalURL)
    getpoint = check.text[int(check.text.index("Point:")) + 6]
    getmesse.append(gfont2.render(getpoint, True, (0,0,0)))

    if getpoint >= questionnum:
        rec_color = [190,255,205]
        getmesse.append(gfont3.render(u"景品交換可能です！", True, (0,0,0)))
        getmesse.append(gfont3.render(u"本部へお越しください", True, (0,0,0)))
        
    else:
        rec_color = [255,153,153]
        if ans == 0:
            getmesse.append(gfont1.render(u"他のスタンプも", True, (0,0,0)))
            getmesse.append(gfont1.render(u"探してみよう！", True, (0,0,0)))

        else:
            getmesse.append(gfont1.render(u"問題をもう1回", True, (0,0,0)))
            getmesse.append(gfont1.render(u"解いてみよう！", True, (0,0,0)))

    while True:
        end = time.time() - start
        if end >= 4:         
            sys.exit(True)

        screen.fill((255,255,255))
        pygame.draw.rect(screen, (rec_color[0], rec_color[1], rec_color[2]), Rect(180,  10, 186, 150))
        screen.blit(stamp, (470,140))

        for i in range(len(getmesse)):
                screen.blit(getmesse[i], (getmessepos[i][0], getmessepos[i][1]))
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == QUIT:       
                 pygame.quit()       
                 sys.exit()

#-----------------------------------------------------------------------------------------#
# 関数 - 登録を求める画面 #
#
# 登録されていないときに出る画面
# 3秒後にsystem.exit

def reqreg():
    start = time.time()
    while True:
        end = time.time() - start
        if end >= 3:         
            #main()
            pygame.quit()
            sys.exit(True)
            break
        
        screen.fill((255,255,255))
        for i in range(len(plsreg)):
                screen.blit(plsreg[i], (plsregpos[i][0], plsregpos[i][1]))
        screen.blit(hanko, (600,240))
        pygame.display.update()
        
        for event in pygame.event.get():
                if event.type == QUIT:       
                    pygame.quit()       
                    sys.exit()

#-----------------------------------------------------------------------------------------#
# 関数 - 既に解かれているとき #
#
# サーバのホームページにIDで問い合わせ, 既に解かれているかどうかチェック.
# 正解数に応じてメッセージ変化.
# 3秒後にsystem.exit


def alsolve():
    start = time.time()
    session = requests.session()
    URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/master.php?IDm="
    totalURL = URL + ID
    check = session.get(totalURL)
    getpoint = check.text[int(check.text.index("Point:")) + 6]
    
    getmesse2 = myfont1.render(u"/ 2 スタンプ獲得済みです", True, (0,0,0))
    getmesse3 = myfont1.render(getpoint, True, (0,0,0))

    if getpoint >= questionnum:
        getmesse4 = myfont2.render(u"本部へ景品交換しに行こう！", True, (0,0,0))
    else:
        getmesse4 = myfont2.render(u"他のスタンプを獲得しにいこう！", True, (0,0,0))


    
    while True:
        end = time.time() - start

        if end >= 3:         
            #main()
            pygame.quit()
            sys.exit(True)
            break
        
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (190,255,205), Rect(40, 300, 740, 100))
        for i in range(len(alsol)):
                screen.blit(alsol[i], (alsolpos[i][0], alsolpos[i][1]))
        screen.blit(getmesse2, (110,320))
        screen.blit(getmesse3, (60, 320))
        screen.blit(getmesse4, (30, 230))
        screen.blit(taihen, (550,20))
        pygame.display.update()
        
        for event in pygame.event.get():
                if event.type == QUIT:       
                    pygame.quit()       
                    sys.exit()  

#-----------------------------------------------------------------------------------------#
# 関数 - IDを特定する #
#
# 読み取りの詳しくはICAS割引参照.
# 読み取ったあとはサーバ登録 -> logserv

def defineID():
    global ID
    try:
        hoge = readICCard.readICCard()
        ID = hoge.getIDM()
        logserv()
    except IOError:
        print("iccard can't read")


#-----------------------------------------------------------------------------------------#
# 関数 -　サーバに登録 #
#
# payloadにサーバのホームページのログインに必要なものを記載.
# トークンも追加し, まとめてpostしログイン.
# 登録状況に応じて関数遷移.

def logserv():
    payload = {
    'email': 'root@fun.ac.jp',
    'password': 'project9',
    }

    session = requests.session()
    tokenr = session.get("http://192.168.2.253/sr_lbs/public_html/login.php", verify=False)
    soup = BeautifulSoup(tokenr.text)
    token = soup.find(attrs = {'name': 'token'}).get('value')
    payload['token'] = token

    logg = session.post("http://192.168.2.253/sr_lbs/public_html/login.php", data = payload, verify=False)

    #ID = "fukke"
    print(ID)
    URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/search.php?node=1&IDm="
    totalURL = URL + ID
    sevtext = session.get(totalURL)

    if sevtext.text.count(u"このIDは存在しません") == 1:
        reqreg()
    elif sevtext.text.count(u"回答済み") == 1:
       alsolve()

#-----------------------------------------------------------------------------------------#
# 関数 - 問題画面 #
#
# 引数 num の数字によって問題番号割り振り.
# タクトスイッチをつないでいないときにめんどいので
# キーボード0 or 1で正解不正解にいける.

def questions(num):

    if num == 1:
        while True:
            screen.fill((255,255,255))
            pygame.draw.rect(screen, (190,255,205), Rect(10,10,780,110))
            for i in range(len(qms1)):
                screen.blit(qms1[i], (qms1pos[i][0], qms1pos[i][1]))
            pygame.display.update()

            if GPIO.input(22) == 0:
                CountDown(1) #A
            if GPIO.input(23) == 0:
                CountDown(0) #B  answer
            if GPIO.input(24) == 0:
                CountDown(1) #C
  
            for event in pygame.event.get():
                if event.type == QUIT:       
                    pygame.quit()       
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_0:
                        CountDown(0)
                    elif event.key == K_1:
                        CountDown(1)
                

    elif num == 2:
        while True:
            screen.fill((255,255,255))
            for i in range(len(qms2)):
                screen.blit(qms2[i], (qms2pos[i][0], qms2pos[i][1]))
            for i in range(3):
                screen.blit(robot, (robotpos[i][0], robotpos[i][1]))
            pygame.display.update()

            if GPIO.input(22) == 0:
                CountDown(1) #A
            if GPIO.input(23) == 0:
                CountDown(1) #B
            if GPIO.input(24) == 0:
                CountDown(0) #C  answer
            
            for event in pygame.event.get():
                if event.type == QUIT:       
                    pygame.quit()       
                    sys.exit()

                    """
                    if event.type == KEYDOWN:
                        if event.key == K_0:
                            CountDown(0)
                        elif event.key == K_1:
                            CountDown(1)
                    """

    elif num == 3:
        while True:
            screen.fill((255,255,255))
            pygame.draw.rect(screen, (190,255,205), Rect(10,10, 560,155))
            for i in range(len(qms3)):
                screen.blit(qms3[i], (qms3pos[i][0], qms3pos[i][1]))
            screen.blit(milky, (610,40))
            screen.blit(mushiba, (600,270))
            pygame.display.update()

            if GPIO.input(22) == 0:
                CountDown(1) #A
            if GPIO.input(23) == 0:
                CountDown(0) #B  answer
            if GPIO.input(24) == 0:
                CountDown(1) #C
                
            for event in pygame.event.get():
                if event.type == QUIT:       
                    pygame.quit()       
                    sys.exit()

                    """
                    if event.type == KEYDOWN:
                        if event.key == K_0:
                            CountDown(0)
                        elif event.key == K_1:
                            CountDown(1)
                    """

#-----------------------------------------------------------------------------------------#
# メイン関数 #
#
# loopでIDが読まれるまでずっと回る.
# question(n)で問題分岐.
# 問題数を増やす場合はrand

def main():
    global ID, rand
    while True:
        screen.fill((255,255,255)) 
        screen.blit(stamp, (450,140))
        for i in range(len(icmesse)):
            screen.blit(icmesse[i], (icmessepos[i][0], icmessepos[i][1])) 
        pygame.display.update()  

        defineID()

        #ID = "011203123D180320"
        if ID != "":
            rand = int((random.random()*100))%3 + 1
            questions(1)

        
        for event in pygame.event.get():
            if event.type == QUIT:  
                pygame.quit()     
                sys.exit()
                

if __name__ == "__main__":
    main()
