# -*- coding: utf-8 -*-

#######################################
#                                                                                                   #
#   This RASPBERRY PI  is MASTER of STAMPRALLY      #
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
import requests
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

pygame.init()                                  
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Master")
ID = ""
point = 0
#png  = ""

allfont = pygame.font.Font("ipaexg.ttf", 50)
pfont = pygame.font.Font("ipaexg.ttf", 80)

nowloading1 = allfont.render(u"ICカード", True, (0,0,0))
nowloading2 = allfont.render(u"読み取り中…", True, (0,0,0))
OK = allfont.render(u"登録完了", True, (0,0,0))
gettedpoint = allfont.render(u"You have            point", True, (0,0,0))
used = allfont.render(u"景品交換済みです。", True, (0,0,0))
prizeexchange = pfont.render(u"景品交換OKです!!", True, (0,0,0))


def pnging(filename):
    global png
    png = pygame.image.load(file_path + filename).convert()
    colorkey = png.get_at((0,0))
    png.set_colorkey(colorkey, RLEACCEL)

    return png



def Register():
    global point
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
    URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/master.php?IDm="
    #http://192.168.2.253/sr_lbs/public_html/icas_discount/master.php?IDm=
    totalURL = URL + ID
    regtext = session.get(totalURL)

    if regtext.text.count(u"結果照会"):
        point = (regtext.text[int(regtext.text.index("Point:")) + 6])
        URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/exchange.php?IDm="
        check = session.get(URL + ID + "&point=3")
        #print(check.text)
        if check.text.count(u"満たしています") == 1:
            URL = "http://192.168.2.253/sr_lbs/public_html/icas_discount/userdelete.php?IDm="
            session.get(URL + ID)
            exchange()
        elif check.text.count(u"本日は交換済みです") == 1:
            today()
            
        result(point)
    else:
        canregister()


def defineID():
    global ID
    try:
        hoge = readICCard.readICCard()
        ID = hoge.getIDM()
        Register()
    except IOError:
        print("iccard can't read")

def result(point):
     while True:
        screen.fill((255,255,255))
        screen.blit(gettedpoint, (150,200))
        pointing = pfont.render(point, True, (0,0,0))
        screen.blit(pointing, (450,180))
        pygame.display.update()     

        for event in pygame.event.get():
            if event.type == QUIT:       
                pygame.quit()       
                sys.exit()

def canregister():
    while True:
        screen.fill((255,255,255))
        screen.blit(OK, (120,200))
        pygame.display.update()     

        for event in pygame.event.get():
            if event.type == QUIT:       
                pygame.quit()       
                sys.exit()

def exchange():
    global png
    pnging("party_cracker.png")

    png2 = pygame.transform.flip(png, 1, 0)
    while True:
        screen.fill((255,255,255))
        screen.blit(prizeexchange, (100,70))
        screen.blit(png, (-100,150))
        screen.blit(png2, (530,150))
        pygame.display.update()     

        for event in pygame.event.get():
            if event.type == QUIT:       
                pygame.quit()       
                sys.exit()

def today():
    while True:
        screen.fill((255,255,255))
        screen.blit(uesd, (120,200))
        pygame.display.update()     

        for event in pygame.event.get():
            if event.type == QUIT:       
                pygame.quit()       
                sys.exit()

def main():
    global png
    pnging("money_ic_card.png")
    while True:
        screen.fill((255,255,255))
        screen.blit(nowloading1, (50,130))
        screen.blit(nowloading2, (50,230))
        screen.blit(png, (380,70))
        pygame.display.update()     
        defineID()
        #exchange()

        for event in pygame.event.get():
            if event.type == QUIT:       
                pygame.quit()       
                sys.exit()

if __name__ == "__main__":
    main()
