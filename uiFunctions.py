from PyQt5.QtWidgets import QMessageBox

#공백인가 확인
def isBlank(str, txtPos):
    str = str.strip()
    if str == '':
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        text = txtPos + '를 입력해주세요.'
        msg.setText(text)
        msg.exec_()
        return False
    return True

#특수문자있는지 확인
def spChar(str):
    if not str.replace(' ', '').isalnum():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText('Keyword에 특수문자는 입력할 수 없습니다.\n다시 입력하세요.')
        msg.exec_()
        return False
    return True

def wordlimit(str):
    if len(str.replace(' ', '')) > 10:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText("글자 수 초과")
        msg.setInformativeText("10글자 이내로 입력하시오.\n(단, 띄어쓰기 제외)")
        msg.exec_()
        return False
    return True
#youtube 링크 유무 판단
def ytValidate(str):
    if not str.count("youtube"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText("youtube 링크 오류")
        msg.setInformativeText("youtube 링크를 입력하시오")
        msg.exec_()
        return False
    return True
