import audiosplit
import apirequest
import keywordtime 
import audiodownload
import audiosection
import functions
import os
import logging
import sys


def main(num,key,link,accessKey):    
    folderName = functions.folName(num,link)
    print('폴더 이름가져오기 성공')
    
    if not os.path.exists('C:\\KIT\\{}'.format(folderName)): #처음 실행되는 파일이면
        functions.makeFolder(folderName)
        print('폴더 만들기 성공')
        audiodownload.download(num,link,folderName) #음원 파일 다운 & 형식 변환
        print('음원 다운로드 성공')
        InfoList,samplerate,second = audiosection.section(folderName) #구간 시간대 정보 
        print('음원 알고리즘 성공')
        audiosplit.split(InfoList,samplerate,folderName) #구간 분할
        print('음원 분할 성공')
        apirequest.request(InfoList,folderName,num,accessKey) #api 요청
        print('음원 api요청 성공')
    second,InfoList = functions.getInfo(folderName)
    print('second,infolist 정보 가져오기 성공')
    allkey,allfreq = keywordtime.time(InfoList,key,second,folderName) #키워드에 의한 텍스트 출력
    print('키워드 시간대 추출 성공')
    return allkey,allfreq



