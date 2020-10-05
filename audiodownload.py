import subprocess
import youtube_dl
from pydub import AudioSegment
import os
import logging
#from PyQt5.QtWidgets import QMessageBox
from tkinter import messagebox as msg
from tkinter import Tk
import sys
import shutil
#내용
"""
url이나 파일경로 선택 변수, url or 파일 경로, 폴더명을 입력받아
유튜브 동영상 다운 후 음원변환 or 음원 변환
"""


def download(num,link,dirname):
    # 5-1 동영상파일 오디오로 변환 ffmpeg 사용
    try:
        if num==1 or num==2:
            command = 'ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn "C:\\KIT\\{}\\temp\\filename.wav"'.format(link,dirname)
            subprocess.call(command, shell=True)
            #동영상 파일 wmv 변환
            
            command = 'ffmpeg -i {} -c:v wmv2 -b:v 20M -c:a wmav2 -b:a 192k "C:\\KIT\\{}\\file\\filename.wmv"'.format(link,dirname)
            subprocess.call(command, shell=True)
                
            # 5-2 음성파일인 경우는 바로 진행
         
            # 5-3 유튜브로부터 wav 추출, ffmpeg 사용
        if num==3:
            try:
                youtubeLink = link #다운 받을 유튜브 링크
                command="youtube-dl -o C:\\KIT\\{}\\temp\\filename.mp3 -x --audio-format mp3 --audio-quality 0 {}".format(dirname,youtubeLink)
                subprocess.call(command.split(),shell=True)
                
                
            #mp3 wav로 변환
            #통일성을 위해 채널을 stereo로해서 wav로  변환한다.
            
                    
                command ="ffmpeg -i C:\\KIT\\{}\\temp\\filename.mp3 -acodec pcm_s16le -ac 2 -ar 16000 C:\\KIT\\{}\\temp\\filename.wav".format(dirname,dirname)
                subprocess.call(command, shell=True)
            except Exception as Herr:
                if os.path.isdir('C:\\KIT\\{}'.format(dirname)):
                    shutil.rmtree('C:\\KIT\\{}'.format(dirname))

                logging.basicConfig(filename='C:\\KIT\\log.log'.format(dirname),level=logging.WARNING)
                logging.error('3. audiodownload 오류')
                logging.error(Herr)

                root = Tk()
                root.withdraw()
                msg.showerror("Error", "오류 발생!\nYoutube Link 오류")
                sys.exit()
                

    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(dirname)):
            shutil.rmtree('C:\\KIT\\{}'.format(dirname))
        
        logging.basicConfig(filename='C:\\KIT\\log.log'.format(dirname),level=logging.WARNING)
        logging.error('3. audiodownload 오류')
        logging.error(err)
        root = Tk()
        root.withdraw()
        msg.showerror("Error", "오류 발생!\n음성 파일 다운로드 오류")
        sys.exit()
