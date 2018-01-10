#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/usr/local/src/nfcpy')
import binascii
import os
import struct
import nfc

class readBIN:
    useHistory = [0 for i in range(20)]
    entryHistory = [0 for i in range(3)]
    
    @classmethod
    def __init__(cls):
        clf = nfc.ContactlessFrontend('usb')
        clf.connect(rdwr={'on-connect': readBIN.connected})

    @classmethod
    def connected(cls, tag):
        service_code_record= 0x108f
        service_code_used= 0x090f

        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            try:
                scr = nfc.tag.tt3.ServiceCode(service_code_record >> 6 ,service_code_record& 0x3f)
                scu = nfc.tag.tt3.ServiceCode(service_code_used >> 6 ,service_code_used & 0x3f)

                #利用履歴
                for i in range(20):
                    uList = []
                    bc = nfc.tag.tt3.BlockCode(i,service=0)
                    datau = tag.read_without_encryption([scu],[bc])
                    for z in datau:
                        uList.append(z)
                    cls.useHistory[i] = uList


                #入場履歴
                for i in range(3):
                    rList = []
                    bc = nfc.tag.tt3.BlockCode(i,service=0)
                    datar = tag.read_without_encryption([scr],[bc])
                    cls.entryHistory[i] = datar
                    for z in datar:
                        rList.append(z)
                    cls.entryHistory[i] = rList

            except Exception as e:
                print "error: %s" % e
        else:
            print "error: tag isn't Type3Tag"

    @classmethod
    def getUseHistory(cls):
        return cls.useHistory

    @classmethod
    def getEntryHistory(cls):
        return cls.entryHistory
