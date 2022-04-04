#!/usr/bin/env python

#
#
#
#

from inspect import EndOfBlock
import signal
from time import sleep
from sys import exit
import random
from array import *
import sys
tmp_x, tmp_y = (0, 0)



class Board():

    board = []
    def board_init(x, y):
        for i in range(x):
            Board.board.append(['_'] * y)

    def display_board():
        def parseRow(row):
            rowStr = ""
            for r in range(len(row)):
                if (row[r] == '_'):
                    row[r] = '.'
                rowStr += row[r]
            return rowStr
        for i in range(len(Board.board)):
            print(parseRow(Board.board[i]), flush=True)
         

    def playerTurn(x, y):
        Board.board[x][y] = 'o'
    
    def brainTurn(x, y):
        Board.board[x][y] = 'x'

    def putDebugPos(xy, symbol):
        x, y = xy
        Board.board[x][y] = str(symbol)

    def getBoard():
        return Board.board

    def getSize():
        return(len(Board.board))

    def deleteBoard():
        Board.board = []

def myReverseSort(tab):
    tmp = []
    for i in range(len(tab) - 1):
        for _i in range(len(tab) - 1):
            x = tab[_i][1]
            y = tab[_i + 1][1]
            if (x<y):
                tmp = tab[_i]
                tab[_i] = tab[_i + 1]
                tab[_i + 1] = tmp
    return tab

class Rules:

    _timeout_turn = 0
    _timeout_match = 0
    _max_memory = 0
    _timeout = 0
    _game_type = 0
    _rule = 0
    _evaluate = 0
    _folder = ""

## BRAIN ##

class Brain:
    isGameStarted = False
    isMatchOpened = False

    postab = []
    _postab = []

    def init_board(x):
        Board.board_init(x, x)

    def brain_start(value):
        Board.board_init(value, value)
        print("OK - everything is good", flush=True)

    def brain_turn():
        x, y = getBestPosition()
        Board.brainTurn(x, y)
        print(str(y) + "," + str(x), flush=True)
        Brain.postab = []
        Brain._postab = []

    def brain_about():
        print('name="Niewtone", version="1.0", author="VictorPierre", country="France"', flush=True)
    
    def brain_end():
        Brain.postab = []
        Brain._postab = []
        Board.deleteBoard()
        Brain.isGameStarted = False
        Brain.isMatchOpened = False
        sys.exit(0)

    def brain_begin():
        _board = Board.getBoard()
        _pos = random.randint(0, Board.getSize() * Board.getSize())
        _x = 0
        for i in range(len(_board)):
            for _i in range(len(_board)):
                _x += 1
                if (_x == _pos):
                    Board.brainTurn(i, _i)
                    print(str(i) + "," + str(_i), flush=True)
                    return


def getBestPosition():
    getAllStickyPosition()
    model = myReverseSort(Brain.postab)
    _model = myReverseSort(Brain._postab)
    bestpos = []

    for i in range(len(model)):
        bestpos.append(model[i])
    for _i in range(len(_model)):
        bestpos.append(_model[_i])

    # debugWeight(bestpos)

    bestpos = myReverseSort(bestpos)

    if (bestpos[0][1] == 0):
        i = random.randint(0, len(bestpos))
        return(bestpos[i][0])
    # print(str(_model) + str(len(_model)))
    if len(_model) > 0:
        if (model[0][1] <= _model[0][1]):
            return(_model[0][0])

    return(bestpos[0][0])
    

def getAllStickyPosition():
    _board = Board.getBoard()
    for i in range(len(_board)):
        for _i in range(len(_board[i])):
            if _board[i][_i] == "o":
                getArroundPositions(i, _i, 'o')
            if _board[i][_i] == "x":
                getArroundPositions(i, _i, 'x')

def debugWeight(tab):

    for i in range(len(tab)):
        if not tab[i][1] == 0:
            Board.putDebugPos(tab[i][0], tab[i][1])

def getArroundPositions(x, y, symbol):
    veski = ''
    if symbol == 'o': veski = 'x'
    else: veski = 'o'

    no(x - 1, y - 1, 1, symbol, veski)
    n(x - 1, y, 1, symbol, veski)
    ne(x - 1, y + 1, 1, symbol, veski)
    e(x, y + 1, 1, symbol, veski)
    o(x, y - 1, 1, symbol, veski)
    so(x + 1, y - 1, 1, symbol, veski)
    s(x + 1, y, 1, symbol, veski)
    se(x + 1, y + 1, 1, symbol, veski)


def no(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        no(x - 1, y - 1, w, symbol, veski)
    else:
        if (_board[x - 1][y - 1] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

def n(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        n(x - 1, y, w, symbol, veski)
    else:
        if (_board[x - 1][y] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

def ne(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        ne(x - 1, y + 1, w, symbol, veski)
    else:
        if (_board[x - 1][y + 1] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

def e(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        e(x, y + 1, w, symbol, veski)
    else:
        if (_board[x][y + 1] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

def o(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        o(x, y - 1, w, symbol, veski)
    else:
        if (_board[x][y - 1] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

def so(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        so(x + 1, y - 1, w, symbol, veski)
    else:
        if (_board[x + 1][y - 1] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

def s(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        s(x + 1, y, w, symbol, veski)
    else:
        if (_board[x + 1][y] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

def se(x, y, w, symbol, veski):
    _board = Board.getBoard()
    if x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1:
        return
    elif _board[x][y] == veski:
        return
    elif _board[x][y] == symbol:
        w += 1
        se(x + 1, y + 1, w, symbol, veski)
    else:
        if (_board[x + 1][y + 1] == symbol):
            if not (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
                w+=1
        if symbol == 'o':
            Brain.postab.append([(x, y), w])
        if symbol == 'x':
            Brain._postab.append([(x, y), w])

## - ##

## COMMANDS ##

class cmds():
    def send_command(_cmd):
        # Rules.rulesChecker()
        cmd = _cmd.split(" ", 1)[0]
        if cmd == "START":
            _Start(_cmd)
        elif cmd == "TURN":
            _Turn(_cmd)
        elif cmd == "BEGIN":
            _Begin()
        elif cmd == "BOARD":
            _Board(_cmd)
        elif cmd == "INFO":
            _Info(_cmd)
        elif cmd == "END":
            _End()
        elif cmd == "ABOUT":
            _About()
        elif cmd == "DISPLAY":
            _Display()
        else:
            return

def _Start(string):
    size = 0
    try:
        string.split(" ", 1)[1]
        isinstance(int(string.split(" ", 1)[1]), int)
        if (isinstance(int(string.split(" ", 1)[1]), int)):
            size = int(string.split(" ", 1)[1])
            if (size == 0):
                print("ERROR bad size", flush=True)
                return
            Brain.isGameStarted = True
            Brain.brain_start(size)
    except:
        print("ERROR message - unsupported size or other error", flush=True)

def _Turn(string):
    value = ""
    x = 0
    y = 0
    try:
        value = string.split(" ", 1)[1]
        x = value.split(",", 1)[0]
        y = value.split(",", 1)[1]
        if (not isinstance(int(y), int)): return
        if (not isinstance(int(y), int)): return
    except:
        print("ERROR message - unsupported size or other error", flush=True)
        return

    if (Brain.isGameStarted == False): return
    if (Brain.isMatchOpened == False):
        Brain.isMatchOpened = True
    if int(x) < 0 or int(x) > Board.getSize() - 1 or int(y) < 0 or int(y) > Board.getSize() - 1:
        return
    if Board.board[int(x)][int(y)] == 'o' or Board.board[int(x)][int(y)] == 'x':
        return
    
    Board.playerTurn(int(x), int(y))
    Brain.brain_turn()

def _Begin():
    if (Brain.isMatchOpened == False and Brain.isGameStarted == True):
        Brain.brain_begin()
        Brain.isMatchOpened = True
    else:
        print("DEBUG the match as allready started or is the game as not been set yet", flush=True)
def _Board(string):
    if (Brain.isGameStarted == False):
        return
    while (1):
        i = input()
        if (i == "DONE"):
            Brain.brain_turn()
            return
        printCmdBoard(i)

def _Info(string):
    try:
        _cmd = string.split(" ", 1)
        print(_cmd)
        cmd = _cmd[1]
        value = _cmd[2]
    except:
        return
    if (cmd == "timeout_match"):
        Rules._timeout_match = int(value)
    if (cmd == "time_left"):
        print(str(Rules._timeout_match))

def _End():
    Brain.brain_end()

def _About():
    Brain.brain_about()

def _Display():
    Board.display_board()

def printCmdBoard(positions):
    pos = positions.split(",")
    x = 0
    y = 0
    player = 0
    try:
        if len(pos) < 3 or len(pos) > 3:
            print("ERRROR bad input", flush=True)
            return
        x = int(pos[0])
        y = int(pos[1])
        player = int(pos[2])
    except:
        print("BAD input", flush=True)
        return

    if (player > 2): return
    if (x < 0 or x > Board.getSize() - 1 or y < 0 or y > Board.getSize() - 1):
        print("ERROR position is out of map", flush=True)
        return
    if (Board.board[y][x] == 'x' or Board.board[y][x] == 'o'):
        print("ERROR position is not empty" + str(x) + " / " + str(y), flush=True)
        return
    if (player == 1):
        Board.board[y][x] = 'o'
    if (player == 2):
        Board.board[y][x] = 'x'

## - ##

#### MAIN ####

class style:
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class game:
    def game_loop():
        while (1):
            try:
                c = input()
                cmds.send_command(c)
            except EOFError:
                break
        
        exit(0)

def handler(signum, frame):
    msg = style.BOLD + " " + '\n' + style.WARNING + "Exit program...\n"
    print(msg, end="", flush=True)
    exit(0)

signal.signal(signal.SIGINT, handler)


game.game_loop()