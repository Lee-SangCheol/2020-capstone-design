 #-*- coding:utf-8 -*-
import urllib3
import json
import base64
import chardet
import ffmpeg
import subprocess
import requests
import os
import sys
import logging
import shutil
from tkinter import messagebox as tkMsg
from tkinter import Tk
import pdb

#내용
"""
InfoList배열을 받아온다 분할된 wave의 갯수만큼 반복하여
각 wave를 pcm으로 변환, api요청하여 텍스트에 집어넣는다
폴더는 음원파일이름, 폴더 안의 텍스트 이름은 음원 시작시간, 텍스트 내용은 api 변환 내용
"""

def request(InfoList,dirname,num,accessKey):
    try:
        number = 0
        while number<len(InfoList)-1:#임의로 숫자 부여
        
            #오디오 파일 pcm 변환
            command = 'ffmpeg -i "C:\\KIT\\{}\\temp\\wav{}.wav" -f s16le -acodec pcm_s16le -ac 1 -ar 16000 "C:\\KIT\\{}\\temp\\pcm{}.pcm"'.format(dirname,number+1,dirname,number+1)
            subprocess.call(command,shell=True)


            #api 요청 정보
            openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
            audioFilePath = "C:\\KIT\\{}\\temp\\pcm{}.pcm".format(dirname,number+1)
            languageCode = "korean"


            #pcm 파일 입력
            file = open(audioFilePath, "rb")
            audioContents = base64.b64encode(file.read()).decode("utf8")
            file.close()


            #json 형식 생성
            requestJson = {
                "access_key": accessKey,
                "argument": {
                    "language_code": languageCode,
                    "audio": audioContents
                }
            }
        
            #api 요청
            http = urllib3.PoolManager()
            response = http.request(
                "POST",
                openApiURL,
                headers={"Content-Type": "application/json; charset=UTF-8"},
                body=json.dumps(requestJson)
            )
            text = response.data.decode('utf-8')#텍스트 받아옴
            if "Daily amount Limit has been exceed!" in text:#api처리도중 일일 한도 초과시
                if os.path.isdir('C:\\KIT\\{}'.format(dirname)):
                    shutil.rmtree('C:\\KIT\\{}'.format(dirname))
                print("일일 사용량 초과(apirequest)")

                root = Tk()
                root.withdraw()
                tkMsg.showerror("Warning", "금일 사용량을 초과했습니다.\n내일 실행해주세요.")
                sys.exit()
                
            f = open("C:\\KIT\\{}\\text\\{}.txt".format(dirname,InfoList[number]), "w")#텍스트 파일 생성
            f.write(text)#텍스트 파일 쓰기
            f.close()
        
            os.remove('C:\\KIT\\{}\\temp\\pcm{}.pcm'.format(dirname,number+1))#pcm 파일 삭제
            os.remove('C:\\KIT\\{}\\temp\\wav{}.wav'.format(dirname,number+1))#wav 파일 삭제
            number = number + 1
        os.remove('C:\\KIT\\{}\\temp\\filename.wav'.format(dirname))#파일 삭제
        if num==3:#유튜브인 경우 mp3파일도 삭제
            os.remove('C:\\KIT\\{}\\temp\\filename.mp3'.format(dirname))#파일 삭제
    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(dirname)):
            shutil.rmtree('C:\\KIT\\{}'.format(dirname))
        logging.basicConfig(filename='C:\\KIT\\log.log',level=logging.WARNING)
        logging.error('6. apirequest 오류')
        logging.error(err)

        root = Tk()
        root.withdraw()
        tkMsg.showerror("Warning", "API 요청 오류입니다.\n다시 시작해주세요.")
        sys.exit()
   
