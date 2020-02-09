import logging
import sys

ver = sys.version_info[0]

if ver < 3:
    _logLevelNames = logging._levelNames
else:
    _logLevelNames = {}
    for (k, v) in logging._levelToName.items():
        _logLevelNames[v] = k

def err_msg(e):
    if ver < 3:
        return e.message
    else:
        return e.msg

if ver < 3:
    tkinter = 'Tkinter'
else:
    tkinter = 'tkinter'