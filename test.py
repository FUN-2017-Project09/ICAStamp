# sudo python test.py

import readICCard
import os
import sys


#color output
def method(x):
    GREEN = '\033[92m'
    ENDC = '\033[0m'
    p = GREEN + '----- ' + x + ' -----' + ENDC
    print(p)

# test
hoge = readICCard.readICCard()
method("getIDM")
print(hoge.getIDM())
method("getUseHistory")
print(hoge.getUseHistory())
method("getEntryHistory")
print(hoge.getEntryHistory())
method("Year-Month-Day")
print(hoge.getYear(0))
print(hoge.getMonts(0))
print(hoge.getDay(0))
method("getProcess")
print(hoge.getProcess(0))
method("getBalance")
print(hoge.getBalance(0))
method("getOperatorCode")
print(hoge.getOperatorCode(0))
#hoge = None
#hoge = readICCard.readICCard()
#hoge.restart()
# test
#del readICCard
#hoge = None
#import readICCard
#hoge = readICCard.readICCard()
#print __file__
##name = [import readICCard, hoge = readICCard.readICCard()]
#os.execv(sys.executable, name)
