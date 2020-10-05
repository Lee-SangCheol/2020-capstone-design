import logging
import os
import sys
import shutil
from tkinter import Tk
from tkinter import messagebox as msg
import window
from PyQt5.QtCore import QCoreApplication


def errorPrint(message):
    #2020.09.10 수정
    root = Tk()
    root.withdraw()
    msg.showerror("Error", message + "\n다시 시작해주세요.")

def folName(num,link):#foldername 받아옴
    try:
        if num==1 or num==2: #실행할 파일이 컴퓨터 내부의 파일인 경우
            folderName = os.path.basename(link.replace('"', ""))
        elif num==3: #실행할 파일이 유튜브 영상인 경우
            folderName = link[-11:]
        return folderName
    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(folderName)):
            shutil.rmtree('C:\\KIT\\{}'.format(folderName))
        logging.basicConfig(filename='C:\\KIT\\{}\\log.log'.format(folderName),level=logging.WARNING)
        logging.error('1. 내부 파일 혹은 경로 따올 때 오류 발생')
        logging.error(err)
        errorPrint('1. 내부 파일 혹은 경로 따올 때 오류 발생')
        
        sys.exit()

def makeFolder(folderName): #폴더 생성
    try:
        if not os.path.isdir('C:\\KIT'):
            os.makedirs('C:\\KIT')
        os.makedirs('C:\\KIT\\{}'.format(folderName)) #폴더 생성
        os.makedirs(os.path.join('C:\\KIT\\{}'.format(folderName),"temp")) #하위 폴더 생성
        os.makedirs(os.path.join('C:\\KIT\\{}'.format(folderName),"text")) #하위 폴더 생성
        os.makedirs(os.path.join('C:\\KIT\\{}'.format(folderName),"file"))
    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(folderName)):
            shutil.rmtree('C:\\KIT\\{}'.format(folderName))
        logging.basicConfig(filename='log.log',level=logging.WARNING)
        logging.error('2. 폴더 생성 오류')
        logging.error(err)
        errorPrint('2. 폴더 생성 오류')
        print(err)
        sys.exit() 


def getInfo(folderName):
    try:
        f=open('C:\\KIT\\{}\\info.txt'.format(folderName),'r') #info.txt에서 second,InfoList 정보 받아옴
        second = int(f.readline()) #정수변환
        InfoList = list(map(int,f.read().split())) #정수리스트변환
        f.close()
        return second,InfoList
    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(folderName)):
            shutil.rmtree('C:\\KIT\\{}'.format(folderName))
        logging.basicConfig(filename='C:\\KIT\\log.log',level=logging.WARNING)
        logging.error('7. 텍스트 정보 불러오기 오류')
        logging.error(err)

        errorPrint('7. 텍스트 정보 불러오기 오류')
        QCoreApplication.instance().quit()
        sys.exit() 

