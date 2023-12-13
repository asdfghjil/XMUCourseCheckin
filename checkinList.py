import json
import requests
import sys

serverUrl = "https://tingke.xmu.edu.cn/app"

def getCheckinList(session, http_header, userInfo, today=True):
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
            'scene': 1,
            'key': 1 if today else 2
        }
        res = session.post(url, data=data, headers=http_header).text
        res = json.loads(res)
        if res['status'] != 1:
            print('get Checkin list failed')
            raise Exception('get Checkin list failed')
        # print(res)
        return res['Rows']

    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Get checkin list failed"
        }, indent=4))
        raise

def printCheckinList(session, http_header, userInfo, today=True, type="签到"):
    rows = getCheckinList(session, http_header, userInfo, today)
    for id, lesson in enumerate(rows):
        print(id)
        print('课程名称：', lesson['kcMc'])
        print('上课时间：', lesson['skSj'])
        print('签到发起情况：', lesson['qdQkMc'])
        print("签到情况：", lesson['xsQdQkMc'] + ('' if lesson['xsQdQk'] == '0' else f"({lesson['skXsStr']})"))
        # print('\n')
    try:
        ckid = int(input("请输入" + type + "课程的序号："))
    except:
        print('输入错误')
        raise Exception('输入错误')
    if ckid < 0 or ckid >= len(rows):
        print('输入错误')
        raise Exception('输入错误')
    return rows[ckid]