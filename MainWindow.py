import sys
import window
import test 
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui 
from PyQt5.QtGui import QFont
import webbrowser as web
import uiFunctions as ui
import os
import shutil
import functions
from PyQt5.QtCore import * 
from tkinter import messagebox as tkMsg
from tkinter import Tk

choose = uic.loadUiType("choose.ui")[0]
class MainWindow(QWidget, choose):
    isGetKey = False
    gChkYoutube = False
    def __init__(self):
        super().__init__()
        self.setupUi(self)
               
        self.btnYoutube.setStyleSheet(
            '''
            QPushButton{font: 75 12.5pt "Arial";}
            QPushButton:hover{color:rgb(255,255,255);image:url(image/youtube.png); border:0px;}
            
            ''')
        self.btnFile.setStyleSheet(
            '''
            QPushButton{font: 75 12.5pt "Arial";}
            QPushButton:hover{color:rgb(255,255,255);image:url(image/folder.png); border:0px;}
            ''')
        
        self.btnETRI.setStyleSheet(
            '''
            QPushButton{color:rgb(0,0,255);font: 8pt "나눔고딕";border-style:flat;text-decoration: underline;}
            QPushButton:hover{font: 9pt "나눔고딕";}
            ''')
        
        QToolTip.setFont(QFont('나눔고딕', 8))
        
        self.btnYoutube.clicked.connect(self.btnYoutube_clicked)
        self.btnFile.clicked.connect(self.btnFile_clicked)

        self.btnETRI.clicked.connect(self.btnETRI_clicked)
        self.btnGetKey.clicked.connect(self.btnGetKey_clicked)
        
        self.mainW = window.Window()
        self.mainH = window.Window()

        
    def btnYoutube_clicked(self):
        try:
            apiKey = self.txtAPIKey.text()
            print(apiKey)
            print(test.keyCheck(apiKey))

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('Error')
            """    
                if test.keyCheck(apiKey)==True:
                    if self.isGetKey == True:#or를and로->이중if문으로 변경 20.08.25->20.09.08 
                    
            """
            if ui.isBlank(apiKey, 'Key'):
                if (self.isGetKey == True) or (test.keyCheck(apiKey) == True):
                    if (test.keyCheck(apiKey) == -2):
                        root = Tk()
                        root.withdraw()
                        tkMsg.showerror("Warning", "금일 사용량을 초과했습니다.")

                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap("image/youtube.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.mainW.setWindowIcon(icon)
                
                    self.mainW.setWindowTitle("키워드 찾기 - Youtube")
                
                    self.mainW.chkYoutube.setChecked(True)

                    self.mainW.txtLink.setEnabled(True)
                    self.mainW.txtLink.setText('')
                    self.mainW.txtKey.setText('')
                    self.mainW.table.setRowCount(0)
                    self.mainW.table.hide()
                    self.mainW.btnPlay.hide()
                    self.mainW.show()
                    self.gChkYoutube = True 
                    
                elif test.keyCheck(apiKey) == -1:
                    print("유효한 키인데 시스템에 문제 발생")
                    msg.setText("시스템에 문제 발생")
                    msg.exec_()
                elif test.keyCheck(apiKey) == -2:#일일 한도 초과시
                    print("일일 사용량 초과")
                    msg.setText("금일 사용량을 초과했습니다.\n내일 실행 해주세요.")
                    msg.exec_()
                else:
                    print("유효한 키가 아님")
                    msg.setText("유효한 키가 아닙니다.\n유효한 키를 입력하세요.")
                    msg.exec_()
        except Exception as e:
            pass
            print(e)
        
    def btnFile_clicked(self):
        try:
            #키 검증 추가
            apiKey = self.txtAPIKey.text()
            print(apiKey)
            print(test.keyCheck(apiKey))
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('Error')
            """    
                if test.keyCheck(apiKey)==True:
                    if self.isGetKey == True:#or를and로->이중if문으로 변경 20.08.25->20.09.08 
             
            """
            if ui.isBlank(apiKey, 'Key'):
                if (self.isGetKey == True) or (test.keyCheck(apiKey) == True):
                    if (test.keyCheck(apiKey) == -2):
                        root = Tk()
                        root.withdraw()
                        tkMsg.showerror("Warning", "금일 사용량을 초과했습니다.")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap("image/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.mainH.setWindowIcon(icon)
                    
                    self.mainH.setWindowTitle("키워드 찾기 - PC")

                    self.mainH.chkYoutube.setChecked(False)
                    self.mainH.btnBrowse.show()
                    self.mainH.txtLink.setEnabled(False)
                    self.mainH.txtLink.setText('')
                    self.mainH.txtKey.setText('')
                    self.mainH.table.setRowCount(0)
                    self.mainH.table.hide()
                    self.mainH.btnPlay.hide()
                    self.mainH.show()
                    self.gChkYoutube = False 
                elif test.keyCheck(apiKey) == -1:
                    print("유효한 키인데 시스템에 문제 발생")
                    msg.setText("시스템에 문제 발생")
                    msg.exec_()
                elif test.keyCheck(apiKey) == -2:#일일 한도 초과시
                    print("일일 사용량 초과")
                    msg.setText("금일 사용량을 초과했습니다.\n내일 실행 해주세요.")
                    msg.exec_()
                else:
                    print("유효한 키가 아님")
                    msg.setText("유효한 키가 아닙니다.\n유효한 키를 입력하세요.")
                    msg.exec_()
                    
        except Exception as e:
            pass
            print(os.path.basename())

    def btnETRI_clicked(self):
        try:
            web.open_new("http://aiopen.etri.re.kr/key_main.php")
        except Exception as ex:
            pass

    def btnGetKey_clicked(self):    
        APIKey = test.getKey()
        if APIKey == False:
            message = QMessageBox.information(self, "ERROR", "저장된 키가 없습니다.\n입력해주세요.")
        else:
            self.txtAPIKey.setEnabled(False)
            self.txtAPIKey.setText(APIKey)
            self.isGetKey = True
    def closeEvent(self,QCloseEvent):
        re=QMessageBox.question(self,"종료 확인","종료하시겠습니까?",QMessageBox.Yes|QMessageBox.No)

        if self.gChkYoutube == True:
            num=3
            link = window.gTxtLink
        else:
            num=1
            link = '"' + window.gTxtLink.replace('/', "\\\\") + '"'

        folderName=functions.folName(num,link)
        print("mainwindow "+folderName+link)
        if re==QMessageBox.Yes:
            print("CloseEvent")
            print(window.bFlag)
            if window.bFlag==True:
                print("<<<유튜브>>>실행중인 쓰레드 확인", self.mainW.work.isRunning())
                print("<<<동영상>>>실행중인 쓰레드 확인", self.mainH.work.isRunning())
                if self.mainW.work.isRunning():
                    self.mainW.work.terminate()
                if self.mainH.work.isRunning():
                    self.mainH.work.terminate()
                    
                if os.path.isfile('C:\\KIT\\{}\\info.txt'.format(folderName)):#youtube다운로드, 동영상wmv변환 완료의 경우
                    if os.path.isfile('C:\\KIT\\{}\\temp\\filename.wav'.format(folderName)):
                        shutil.rmtree('C:\\KIT\\{}'.format(folderName))
                        print('다운또는 변환 완료')
                else:#youtube다운로드중, 동영상wmv변환중
                    if num==3:#유튜부의 경우 1차 중간파일인 filename.mp3과 filename.wav가 없는 경우
                        if not os.path.isfile('C:\\KIT\\{}\\temp\\filename.mp3'.format(folderName)):
                            os.system("taskkill.exe /f /im youtube-dl.exe")
                            shutil.rmtree('C:\\KIT\\{}'.format(folderName))
                            print('유투브1')
                        elif os.path.isfile('C:\\KIT\\{}\\temp\\filename.mp3'.format(folderName)) and os.path.isfile('C:\\KIT\\{}\\temp\\filename.wav'.format(folderName)):#filename.mp3다운로드후 filename.wav로 변환하는 중
                            os.system("taskkill.exe /f /im ffmpeg.exe")        
                            shutil.rmtree('C:\\KIT\\{}'.format(folderName))
                            print('유투브2')
                    elif (num==1 or num==2) and os.path.isfile('C:\\KIT\\{}\\temp\\filename.wav'.format(folderName)):#동영상의 경우 filename.wav가있는 경우
                        os.system("taskkill.exe /f /im ffmpeg.exe")        
                        shutil.rmtree('C:\\KIT\\{}'.format(folderName))
                        print('동영상')

            
            QCloseEvent.accept()
            QCoreApplication.instance().quit()
            
        else:
            QCloseEvent.ignore()
    
      
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())
