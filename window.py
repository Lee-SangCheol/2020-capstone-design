import sys
import main
import time
import videoWidget
import webbrowser as web
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
import test
import uiFunctions as ui
import helpUI

form1 = uic.loadUiType("sub2.ui")[0]    
link = ""

allkey = []
allKeyFreq = []

gTxtLink = ""
gTxtKey = ""
gChkYoutube = False

bFlag = False
class Thread(QThread):
    finish_sign = pyqtSignal()     
    
    def bStart(self):
        global gTxtLink
        global gTxtKey
        global gChkYoutube
        
        if gChkYoutube == True:
            num = 3
            link = gTxtLink
            
        else:
            num = 1
            link = '"' + gTxtLink.replace('/', "\\\\") + '"'

        key = gTxtKey
        print(link)

        global allkey
        global allKeyFreq
        print(link)
        accessKey=test.getKey()
        allkey, allKeyFreq = main.main(num, key, link, accessKey)


        print(allkey, allKeyFreq)

    def run(self):
        global bFlag
        print('run')
        bFlag=True
        print(bFlag)
        self.bStart()
        self.finish_sign.emit()

    
class Window(QMainWindow, form1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("키워드 찾기")
        self.chkYoutube.hide()  
        self.lblErr.hide()    

        
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        
        self.btnBrowse.clicked.connect(self.btnBrowse_clicked)
        self.btnStart.clicked.connect(self.btnStart_clicked)

        self.table.cellDoubleClicked.connect(self.table_cellDoubleClicked)
        self.btnPlay.clicked.connect(self.table_cellDoubleClicked) 
        
        self.work = Thread()
        self.work.finish_sign.connect(self.finish_sign_emitted)

        #사용법(helpAction)
        helpAction = QAction(QIcon('help.png'), '&Help', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip('How to use')
        helpAction.triggered.connect(self.openHelp)

        menuBar = self.menuBar()
        helpMenu = menuBar.addMenu('&Help(H)')
        helpMenu.addAction(helpAction)

          

    """
    새로운 파일이 선택되거나 새로운 url이 입력되면
    txtLink를 제외한 모든 위젯 초기화되어야함.
    """
    def btnBrowse_clicked(self):
        if self.chkYoutube.isChecked() == False:
            text = QFileDialog.getOpenFileName(self, 'Open File', "", "video files(*.mp4  *.wmv  *.wav);;All files(*.*)")
            self.txtLink.setText(text[0])

        else:
            web.open_new("www.youtube.com")


    def btnStart_clicked(self):
        
        self.table.hide()
        self.btnPlay.hide()
        
        global gTxtLink
        global gTxtKey
        global gChkYoutube
        gChkYoutube = self.chkYoutube.isChecked()
        gTxtLink = self.txtLink.text()
        gTxtKey = self.txtKey.text()
        
        if ui.isBlank(gTxtLink, 'Path/Url') and ui.isBlank(gTxtKey, 'Keyword'):
            if ui.spChar(gTxtKey) and ui.wordlimit(gTxtKey):                    
                if gChkYoutube and ui.ytValidate(gTxtLink):
                    self.work.start()
                    self.lblErr.setText("Please wait...")
                    self.lblErr.show()
                    self.txtLink.setEnabled(False)
                    self.txtKey.setEnabled(False)
                    self.btnStart.setEnabled(False)
                elif not gChkYoutube:
                    self.work.start()
                    self.lblErr.setText("Please wait...")
                    self.lblErr.show()
                    self.txtLink.setEnabled(False)
                    self.txtKey.setEnabled(False)
                    self.btnStart.setEnabled(False)
                    self.btnBrowse.setEnabled(False)

    @pyqtSlot()
    def finish_sign_emitted(self):
        global bFlag
        bFlag = False
        self.txtLink.setEnabled(True)
        self.txtKey.setEnabled(True)
        self.btnStart.setEnabled(True)
        if self.chkYoutube.isChecked() == False:
            self.btnBrowse.setEnabled(True)
            self.txtLink.setEnabled(False)

        self.lblErr.hide()

        if self.chkYoutube.isChecked() == False:
            self.btnBrowse.setEnabled(True)
        
        global allkey
        global allKeyFreq

        print("start!!!!", allkey, allKeyFreq)
        self.table.setRowCount(len(allkey))

        self.table.setColumnWidth(0,100)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(2,554)
        print('123123132')
        for i in range(self.table.rowCount()):
            self.table.setItem(i, 0, QTableWidgetItem(str(allkey[i]) + 's'))
            self.table.setItem(i, 1, QTableWidgetItem(str(allKeyFreq[i])))
            self.table.item(i, 0).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.item(i, 1).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        
        self.table.show()
        print('1231231321')

        self.btnPlay.show()


    def table_cellDoubleClicked(self):
        sltInfo = self.table.selectedIndexes()
        index = sltInfo[0].row()
        sec = self.table.item(index, 0).text()

        link = self.txtLink.text()
        if self.chkYoutube.isChecked() == True:
            link += "&t=" + sec
            web.open_new(link)
        else:
            self.videoWindow = videoWidget.VideoWindow()
            tempLink = link.replace("/", "\\\\")

            if ".mp4" in tempLink:
                temp_list = tempLink.split("\\")
                temp_list = temp_list[-1:]
                tempLink = "C:\\KIT\\{}\\file\\filename.wmv".format("\\".join(temp_list))
                
            print(tempLink)
            self.videoWindow.openLink(tempLink)
            print(int(sec.replace("s","")))
            self.videoWindow.setPosition(int(sec.replace("s", "")) * 1000)
            self.videoWindow.resize(640, 480)
            self.videoWindow.btnPlay_clicked()
            self.videoWindow.show()



    def openHelp(self):
        self.help = helpUI.help()
        self.help.show()

    def closeEvent(self, QCloseEvent):
        global bFlag

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        if bFlag == True:
            msg.setText("실행 중에는 창을 닫을 수 없습니다.")
            msg.exec_()
            QCloseEvent.ignore()
        else:
            QCloseEvent.accept()

