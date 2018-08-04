from _winreg import *
import string
import datetime
from datetime import *

loc_ = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList"

def get_subkeys(key):
    for i in range(QueryInfoKey(key)[0]):
        name = EnumKey(key,i)
        yield(name,OpenKey(key,name))

def time_convert(ns):
    return datetime(1601, 1, 1) + dt.timedelta(seconds=ns/1e7)

with OpenKey(HKEY_LOCAL_MACHINE, loc_, 0, KEY_READ | KEY_WOW64_64KEY) as NetList:
    for subkey in get_subkeys(NetList):
            print(subkey)
            modtime = time_convert(QueryInfoKey(subkey[1])[2])
            print u"\n\n{}:modified{}".format(subkey[0],modtime)