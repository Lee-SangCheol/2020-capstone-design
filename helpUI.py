import sys
import window
import test 
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui 
from PyQt5.QtGui import QFont 
import webbrowser as web 
import uiFunctions as ui

helpUI = uic.loadUiType("help.ui")[0]

class help(QMainWindow, helpUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_7.setPixmap(QtGui.QPixmap("image/helpimg2.png"))
        
        
