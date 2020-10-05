from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
import os

class VideoWindow(QMainWindow):
    def __init__(self, parent = None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Example")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.btnPlay = QPushButton()
        self.btnPlay.setEnabled(False)
        self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.btnPlay.clicked.connect(self.btnPlay_clicked)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0,0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        #사운드 버튼 생성
        self.btnSound = QPushButton()
        self.btnSound.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.btnSound.clicked.connect(self.btnSound_clicked)
        #사운드용 수평슬라이드바 생성
        self.soundpositionSlider = QSlider(Qt.Horizontal)
        self.soundpositionSlider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        #0부터 100까지 칸 수만큼 슬라이드 할 수 있는 바 생성
        self.soundpositionSlider.setRange(0, 100)
        self.soundpositionSlider.setValue(100)
        self.soundpositionSlider.sliderMoved.connect(self.setsoundPosition)
    

        #create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        #create new action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)
        
        #create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        #create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        #create layouts to place inside widget 수평으로 추가
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.btnPlay)
        controlLayout.addWidget(self.positionSlider)

        soundLayout = QHBoxLayout()
        soundLayout.addWidget(self.btnSound)
        soundLayout.addWidget(self.soundpositionSlider)
        soundLayout.setContentsMargins(500, 0, 0, 0) #(left, top, right, bottom)


        #레이아웃 생성 후 수직 순서로 레이아웃 추가
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addLayout(soundLayout)   
        layout.addWidget(self.errorLabel)

        #set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "Video Files (*.avi *.mp4 *.wav);;All Files (*.*)")

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName.replace('/', '\\\\'))))
            self.btnPlay.setEnabled(True)

    ##전달       
    def openLink(self, Link):
        if Link != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Link)))
            self.btnPlay.setEnabled(True)
                       
    def exitCall(self):
        self.mediaPlayer.pause()
        self.close()
        
    def btnPlay_clicked(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.btnPlay.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Question", "창을 닫으시겠습니까?")
        if message == QMessageBox.Yes:
            self.mediaPlayer.pause()
            event.accept()
        else:
            event.ignore()


    def btnSound_clicked(self):
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            self.btnSound.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.mediaPlayer.setMuted(True)
            self.btnSound.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))

    def setsoundPosition(self, position):
        self.mediaPlayer.setVolume(position)

