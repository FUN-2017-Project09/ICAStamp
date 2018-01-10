#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import binascii
import os
import struct
import sys

sys.path.append('/usr/local/src/nfcpy')
import nfc

num_blocks = 20
service_code = 0x090f

class StationRecord(object):
  db = None

  def __init__(self, row):
    self.area_key = int(row[0], 10)
    self.line_key = int(row[1], 10)
    self.station_key = int(row[2], 10)
    self.company_value = row[3]
    self.line_value = row[4]
    self.station_value = row[5]

  @classmethod
  def get_none(cls):
    # 駅データが見つからないときに使う
    return cls(["0", "0", "0", "None", "None", "None"])
  @classmethod
  def get_db(cls, filename):
    # 駅データのcsvを読み込んでキャッシュする
    if cls.db == None:
      cls.db = []
      for row in csv.reader(open(filename, 'rU'), delimiter=',', dialect=csv.excel_tab):
        cls.db.append(cls(row))
    return cls.db
  @classmethod
  def get_station(cls, line_key, station_key):
    # 線区コードと駅コードに対応するStationRecordを検索する
    for station in cls.get_db("StationCode.csv"):
      if station.line_key == line_key and station.station_key == station_key:
        print "station.line_key：%d" % line_key
        print "station.station_key：%d" % station_key
        return station
    return cls.get_none()

class HistoryRecord(object):
  def __init__(self, data):
    # ビッグエンディアンでバイト列を解釈する
    row_be = struct.unpack('>2B2H4BH4B', data)
    # リトルエンディアンでバイト列を解釈する
    row_le = struct.unpack('<2B2H4BH4B', data)
    print "====== run HistoryRecord ====="
    self.db = None
    self.console = self.get_console(row_be[0])
    self.process = self.get_process(row_be[1])
    self.year = self.get_year(row_be[3])
    self.month = self.get_month(row_be[3])
    self.day = self.get_day(row_be[3])
    self.balance = row_le[8]

    print "===in_station===="
    self.in_station = StationRecord.get_station(row_be[4], row_be[5])
    print "===out_station==="
    self.out_station = StationRecord.get_station(row_be[6], row_be[7])

  @classmethod
  def get_console(cls, key):
    return {
    #ttps://ja.osdn.net/projects/felicalib/wiki/suica
      0x03: "精算機",
      0x04: "携帯型端末",
      0x05: "車載端末",
      0x07: "券売機",
      0x08: "券売機",
      0x09: "入金機",
      0x12: "券売機",
      0x14: "券売機等",
      0x15: "券売機等",
      0x16: "改札機",
      0x17: "簡易改札機",
      0x18: "窓口端末",
      0x19: "窓口端末",
      0x1a: "改札端末",
      0x1b: "携帯電話",
      0x1c: "乗継精算機",
      0x1d: "連絡改札機",
      0x1f: "簡易入金機",
      0x46: "VIEW ALTTE",
      0x48: "VIEW ALTTE",
      0xc7: "物販端末",
      0xc8: "自販機",
      0x1c: "乗継精算機",
      0x1d: "連絡改札機",
      0x1f: "簡易入金機",
      0x46: "VIEW ALTTE",
      0x48: "VIEW ALTTE",
      0xc7: "物販端末",
      0xc8: "自販機",
    }.get(key)
  @classmethod
  def get_process(cls, key):
    return {
      0x06: "窓出 (改札窓口処理)",
      0x07: "新規 (新規発行)",
      0x08: "控除 (窓口控除)",
      0x0d: "バス (PiTaPa系)",
      0x0f: "バス (IruCa系)",
      0x11: "再発 (再発行処理)",
      0x13: "支払 (新幹線利用)",
      0x14: "入A (入場時オートチャージ)",
      0x15: "出A (出場時オートチャージ)",
      0x1f: "入金 (バスチャージ)",
      0x23: "券購 (バス路面電車企画券購入)",
      0x46: "物販",
      0x48: "特典 (特典チャージ)",
      0x49: "入金 (レジ入金)",
      0x4a: "物販取消",
      0x4b: "入物 (入場物販)",
      0xc6: "物現 (現金併用物販)",
      0xcb: "入物 (入場現金併用物販)",
      0x84: "精算 (他社精算)",
      0x85: "精算 (他社入場精算)",
    }.get(key)
  @classmethod
  def get_year(cls, date):
    return (date >> 9) & 0x7f
  @classmethod
  def get_month(cls, date):
    return (date >> 5) & 0x0f
  @classmethod
  def get_day(cls, date):
    return (date >> 0) & 0x1f

def connected(tag):
  print tag

  if isinstance(tag, nfc.tag.tt3.Type3Tag):
    try:
      sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
      for i in range(num_blocks):
        bc = nfc.tag.tt3.BlockCode(i,service=0)
        data = tag.read_without_encryption([sc],[bc])
        history = HistoryRecord(bytes(data))
        print "=== %02d ===" % i
        print "端末種: %s" % history.console
        print "処理: %s" % history.process
        print "日付: %02d-%02d-%02d" % (history.year, history.month, history.day)
        print "入線区: %s-%s" % (history.in_station.company_value, history.in_station.line_value)
        print "入駅順: %s" % history.in_station.station_value
        print "出線区: %s-%s" % (history.out_station.company_value, history.out_station.line_value)
        print "出駅順: %s" % history.out_station.station_value
        print "残高: %d" % history.balance
        print "BIN: "
        print "" . join(['%02x ' % s for s in data])
    except Exception as e:
      print "error: %s" % e
  else:
    print "error: tag isn't Type3Tag"

if __name__ == "__main__":
  clf = nfc.ContactlessFrontend('usb')
  clf.connect(rdwr={'on-connect': connected})
