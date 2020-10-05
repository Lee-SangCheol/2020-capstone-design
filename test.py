import subprocess
import urllib3
import base64
import json
import os


##### txt파일 있으면 무조건 True
#### txt 파일 없을 때 키 값 유효성 검사 -> True / False
### 유효한 키인데 오류뜨면 -1
## 일일 한도 초과하면 2
def keyCheck(accessKey):
    if not os.path.isdir('C:\\KIT'):
        os.makedirs('C:\\KIT')
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    audioFilePath = "test.pcm"
    languageCode = "korean"

    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "language_code": languageCode,
            "audio": audioContents
        }
    }
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    text = response.data.decode('utf-8')#텍스트 받아옴
    
    if "Invalid Access Key" in text:
       return False
    elif "Daily amount Limit has been exceed!" in text:
        return -2
    elif '"result":0' in text:
        f = open('C:\\KIT\\apiKey.txt','w')
        f.write(accessKey)
        f.close()
        return True
    else:
        return -1

###### txt파일 있으면 키 값 리턴 없으면 False 리턴
def getKey():
    if os.path.isfile('C:\\KIT\\apiKey.txt'):
        f = open('C:\\KIT\\apiKey.txt')
        key = f.readline()
        f.close()
        return key
    else:
        return False
