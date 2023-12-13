import json
import requests
import sys
import random

from checkinList import printCheckinList

serverUrl = "https://tingke.xmu.edu.cn/app"
serverImg = "https://tingke.xmu.edu.cn/uploadFile"

def uuid():
    d = "0123456789"
    return "".join([random.choice(d) for i in range(30)])

def getCheckinScanCode(session, http_header, userInfo, checkinID):
    try:
        url = serverUrl + "/getRQCodeInfo"
        t = uuid()
        data = {
            'scene': t,
            'sign': userInfo['sign'],
            'userType': userInfo['userType'],
            'userCode': userInfo['userCode'],
            'unitCode': userInfo['unitCode'],
            'qdId': checkinID
        }
        res_ = session.post(url, data=data, headers=http_header)
        res = json.loads(res_.text)
        if res_.status_code != 200 or res['status'] != 1:
            print('get Checkin scan code failed')
            if res_.status_code == 200:
                print(res['msg'])
            raise Exception('get Checkin scan code failed')
        scanUrl = serverImg + res['src']
        print('分享码链接：', scanUrl)
        return scanUrl, t
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Get checkin scan code failed"
        }, indent=4))
        raise

def scanCodeCheckin(session, http_header, userInfo, checkinID):
    scanUrl, scanCode = getCheckinScanCode(session, http_header, userInfo, checkinID)
    try:
        url = serverUrl + "/getQdKbList"
        data = {
            'sign': userInfo['sign'],
            'userType': userInfo['userType'],
            'userCode': userInfo['userCode'],
            'unitCode': userInfo['unitCode'],
            'userName': userInfo['userName'],
            'roleCode': userInfo['roleCode'],
            'bm': None,
            'xyMc': userInfo['xy'],
            'zy': userInfo['zy'],
            'bj': userInfo['bj'],
            'xsCc': userInfo['xsCc'],
            'scene': scanCode,
            'key': None
        }
        res = session.post(url, data=data, headers=http_header).text
        # print(res)
        res = json.loads(res)
        if res['isScan'] != '1':
            print('scan code checkin failed')
            return
        if res['status'] != 1:
            print('扫码签到失败：', res['msg'])
            return
        print('扫码签到成功')
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Scan code checkin failed"
        }, indent=4))
        return

def scanCheckin(session, http_header, userInfo):
    lesson = printCheckinList(session, http_header, userInfo, today=True)
    scanCodeCheckin(session, http_header, userInfo, lesson['qdId'])