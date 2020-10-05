import sys
import logging
from tkinter import Tk
from tkinter import messagebox as msg
import shutil
#내용
"""
텍스트 파일을 받아와서 입력된 키워드에 대해 구간별 키워드 빈도를 저장후 반환
키워드가 나온 구간을 저장후 반환
"""


def time(infoList,key,second,dirname):
    try:
        allKeyword=[] #키워드 들어간 모든 위치
        allKeywordFreq=[] #키워드 들어간 파일의 키워드 수
        num=0
        keywordInfo=[] #전체 구간마다의 키워드 나온 횟수
        while num<len(infoList)-1:
            f = open("C:\\KIT\\{}\\text\\{}.txt".format(dirname,infoList[num]), 'r') #텍스트 파일로부터 읽어옴
            data = f.read()
            keywordInfo.append(data.count(key)) #일치하는 갯수 저장
            f.close()
            num=num+1

        #키워드 들어가는 모든 위치 값 저장
        num=0
        while num<len(keywordInfo):
            if keywordInfo[num]>0: #그 구간에서 키워드 나온 갯수가 1개 이상이면
                allKeyword.append(infoList[num]//second) #구간의 시작시간 저장
                allKeywordFreq.append(keywordInfo[num])
            num = num + 1

        print(allKeyword, allKeywordFreq)
        return allKeyword, allKeywordFreq #리스트 리턴
    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(dirname)):
            shutil.rmtree('C:\\KIT\\{}'.format(dirname))
        logging.basicConfig(filename='C:\\KIT\\log.log',level=logging.WARNING)
        logging.error('8. keywordtime 오류')
        logging.error(err)
        root = Tk()
        root.withdraw()
        msg.showerror("Error", "키워드 시간 추출 오류입니다.\n다시 시작해주세요.")
        sys.exit()
