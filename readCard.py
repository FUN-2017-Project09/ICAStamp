#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readBIN
import readIDm

#color output
GREEN = '\033[92m'
ENDC = '\033[0m'

x = GREEN + '----- History of use -----' + ENDC
y = GREEN + '----- History of entry' + ENDC
z = GREEN + '----- IDm-----' + ENDC

rbin = readBIN.readBIN()
rbindatause = rbin.getUseHistory()
rbindataentry = rbin.getEntryHistory()
ridm = readIDm.readIDm()

print(x)
print(rbindatause)
print(y)
print(rbindataentry)
print(z)
print(ridm.getIDm())

date = str(format(rbindatause[20][11],'b').zfill(8)) + str(format(rbindatause[19][10],'b').zfill(8))
print(date)
print(int(date,2))
