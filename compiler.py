#!/usr/bin/env python

#
#
#
#

import os

def compile():
    os.system("pyinstaller main.py --name pbrain-gomoku-ai.exe --onefile")

compile()