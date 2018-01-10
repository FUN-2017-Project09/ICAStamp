#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readBIN
import readIDm
from cli import CommandLineInterface

"""
How To Use
インポート:                                           import readICCard
インスタンス生成:                              hoge = readICCard.readICCard() 
データを手に入れる(例は年):          fuga = hoge.getYear(2)]

method一覧
getUseHistory():		    利用履歴20件のバイナリが入った二次元配列
getEntryHistory():  		   入出場履歴３件のバイナリが入った二次元配列
getIDM():			   IDm取得
getYear(履歴番号(max:20)):	   指定した利用履歴の記録年
getMonth(履歴番号(max:20)): 指定した利用履歴の記録月
getDay(履歴番号(max:20)):	   指定した利用履歴の記録日
getProcess(履歴番号(max:20)):指定した利用履歴の利用種別
getBalance(履歴番号(max:20)):指定した利用履歴の残高
getOperatorCode(履歴番号(max:20)):指定した利用履歴の事業者コード
"""

class readICCard:
    
    @classmethod 
    def __init__(cls):
        binary = None
        idm = None
        binary = readBIN.readBIN()
        idm = readIDm.readIDm()
        cls.useHistory = binary.getUseHistory()
        cls.entryHistory = binary.getEntryHistory()
        cls.IDm = idm.getIDm()
        
    @classmethod
    def getUseHistory(cls):
        return cls.useHistory

    @classmethod
    def getEntryHistory(cls):
        return cls.entryHistory

    @classmethod
    def getIDM(cls):
        return cls.IDm

    @classmethod
    def getYear(cls, hisNum):
        if(hisNum >= 20):
            return 0
        date = str(format(cls.useHistory[hisNum][4],'b').zfill(8)) + str(format(cls.useHistory[hisNum][5],'b').zfill(8))
        return int(date[0:7],2)
        
    @classmethod
    def getMonts(cls, hisNum):
        if(hisNum >= 20):
            return 0
        date = str(format(cls.useHistory[hisNum][4],'b').zfill(8)) + str(format(cls.useHistory[hisNum][5],'b').zfill(8))
        return int(date[7:11],2)

    @classmethod
    def getDay(cls, hisNum):
        if(hisNum >= 20):
            return 0
        date = str(format(cls.useHistory[hisNum][4],'b').zfill(8)) + str(format(cls.useHistory[hisNum][5],'b').zfill(8))
        return int(date[11:16],2)

    @classmethod
    def getProcess(cls, hisNum):
        if(hisNum >= 20):
            return 0
        return cls.useHistory[hisNum][1]

    @classmethod
    def getBalance(cls, hisNum):
        if(hisNum >= 20):
            return 0
        balance = str(format(cls.useHistory[hisNum][11],'b').zfill(8)) + str(format(cls.useHistory[hisNum][10],'b').zfill(8))
        return int(balance,2)

    @classmethod
    def getOperatorCode(cls, hisNum):
        code = str(format(cls.useHistory[hisNum][6],'b').zfill(8)) + str(format(cls.useHistory[hisNum][7],'b').zfill(8))
        return int(code,2)

    @classmethod
    def restart(cls):
        test = readIDm.readIDm()
        test.TagTool.run()
