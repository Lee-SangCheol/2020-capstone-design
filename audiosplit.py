import os
import librosa
import sys
import logging
from tkinter import Tk
from tkinter import messagebox as msg
import shutil
#내용
"""
audiosection에서 생성된 InfoList,samplerate,폴더명 정보를 입력받아서
전체 음원 파일을 분리한다
"""


def split(InfoList,samplerate,dirname):
    #음성 자르는 코드
    try:
        y, sr = librosa.load('C:\\KIT\\{}\\temp\\filename.wav'.format(dirname), sr=samplerate) #파일 읽어옴
        number = 0
        while number<=len(InfoList)-2: #분할할 파일 수 반복
            tempWave = y[InfoList[number]:InfoList[number+1]] #각 구간 별 데이터 저장
            librosa.output.write_wav('C:\\KIT\\{}\\temp\\wav{}.wav'.format(dirname,number+1),tempWave,sr) #구간의 음원 추출
            number = number + 1
    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(dirname)):
            shutil.rmtree('C:\\KIT\\{}'.format(dirname))
        logging.basicConfig(filename='C:\\KIT\\log.log',level=logging.WARNING)
        logging.error('5. audiosplit 오류')
        logging.error(err)

        root = Tk()
        root.withdraw()
        msg.showerror("Error", "5. 음원 분리 오류 발생!\n다시 시작해주세요.")
        msg.exec_()        
        sys.exit()
