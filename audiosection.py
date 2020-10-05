import numpy as np 
import scipy.io as sio
import scipy.io.wavfile
import sys
import logging
from tkinter import Tk
from tkinter import messagebox as msg
import os
import shutil
#설명
"""
음원의 시작부터 기준시간 뒤 지점에서부터 앞으로가며 말이 끊어지는 구간을 찾음
예를들어 50초에 처음 끊겼다고 하면 다음은 45초+기준시간에서 줄어들면서 구간을 찾음
배열에 끊기는 구간 정보를 담고 이를 기준으로 음성파일을 나눈다

구간을 나누는 기준 - 0.5초 단위로 진폭의 평균값을 측정한 값이 음원의 최대 진폭 값을
50으로 나눈 값보다 작을 때 그 구간의 중간 인덱스 값

진폭 기준 값과 0.5초 단위로 측정 등의 방법은 수정 가능

info.txt에 second,InfoList 정보 저장
"""


def section(dirname): #link는 파일경로나 유튜브 링크, num은 판단기준    
    #파일 가져오기
    try:
        samplerate, data=sio.wavfile.read('C:\\KIT\\{}\\temp\\filename.wav'.format(dirname))
        data1=data.mean(axis=1)#array로 변환시 dictionary타입으로 변경되기때문에(음성은 stereo이기 때문) 단일로 변경하는 방법 
        tmp1=np.array(data1,dtype=np.int8) #진폭 데이터 일반 값
        tmp2 = np.absolute(tmp1) #진폭 데이터 절대값

        ampMax = np.max(tmp2) #음원 파일의 최대 진폭 값
        ampMin = ampMax/10 #진폭 구간 기준 값 (임의로 설정)(5에서 10으로 수정,20.08.05)


        start = 0 #1분 단위의 구간의 첫 인덱스 값
        end = 0  #기준 단위의 구간의 마지막 인덱스 값
        cur = 0 #기준 시간 단위의 구간 안에서 1초 단위의 구간을 움직이는 값
        temp = 0 #start 위치를 위한 임시 값
        InfoList=[0] #구간 정보를 담는 리스트 시작, 끝 값을 담음
        second = samplerate# 1초의 샘플 갯수    (말 끊기는 기준 탐색 기준 : 1초)
        minute = 45 * second# 기준시간의 샘플 갯수   (음원 분할 1개의 최대 길이 : 30초->45초로 수정 20.08.05)


        while start+minute<len(tmp2): #start 값이 끝에 도달한 경우 (영상 분할이 끝나면)

            end = start + minute #일반적인 경우 end는 start + 기준 시간
            cur = end #cur은 end부터 시작해서 줄어들며 구간을 찾음

            while True: #기준시간 내에서의 반복
                if cur-second <= start: #cur이 start까지 온 경우 (한 구간의 측정이 start까지 온 경우)
                    if np.mean(tmp2[start:cur])<=ampMin: #start부터 cur까지 평균 값이 기준 미만 이면
                        temp = (start + cur)//2 #cur과 start의 중간 인덱스 값
                        InfoList.append(temp) #중간 인덱스 값 리스트에 저장, 다음 구역 탐색
                        break
                    else:  # start까지 왔으나 기준보다 낮은 값을 찾지 못한 경우 끊기는 것 무시하고 end값을 넣어줌
                        InfoList.append(end)
                        temp = end #end를 start로 하여 다음 구역 탐색
                        break
                else :
                    if np.mean(tmp2[(cur-second):cur])<=ampMin: # cur과 cur-기준시간 사이의 평균 값이 기준값 보다 작은 경우
                        temp = (cur*2 - second)//2 #cur과 cur - 0.5초 사이의 중간 인덱스
                        InfoList.append(temp) #중간 인덱스 값을 리스트에 저장
                        break
                    else :
                        cur = cur - second # 구간을 찾지 못한 경우 cur값을 - 0.5초으로 하고 다시 진행
            start = temp #찾은 구간의 중간 인덱스 값을 start로 하여 다시 진행

        InfoList.append(len(tmp2)-1) #끝 값 저장



        #infolist의 내용을 info.txt에 write한다
        f = open('C:\\KIT\\{}\\info.txt'.format(dirname),'w')
        f.write("%s\n" % second)
        for info in InfoList:
            f.write("%s\n" % info)
        f.close()
        return InfoList,samplerate,second
    except Exception as err:
        if os.path.isdir('C:\\KIT\\{}'.format(dirname)):
            shutil.rmtree('C:\\KIT\\{}'.format(dirname))
        logging.basicConfig(filename='C:\\KIT\\log.log',level=logging.WARNING)
        logging.error('4. audiosection 오류')
        logging.error(err)

        root = Tk()
        root.withdraw()
        msg.showerror("Error", "음원 시간대 출력 알고리즘 오류\n다시 시작해주세요.")        
        sys.exit()
    


