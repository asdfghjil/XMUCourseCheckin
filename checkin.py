import json
import requests
import sys
import time
import random

from checkinList import getCheckinList, printCheckinList

serverUrl = "https://tingke.xmu.edu.cn/app"

def getCheckinInfo(session, http_header, userInfo, lesson):
    try:
        url = serverUrl + "/getXsQdInfo"
        data = {
            'sign': userInfo['sign'],
            'unitCode': userInfo['unitCode'],
            'userCode': userInfo['userCode'],
            'userName': userInfo['userName'],
            'xkKh': lesson['xkKh'],
            'qdRq': lesson['qdRq'],
            'xqj': lesson['xqj'],
            'djj': lesson['djj'],
            'djz': lesson['djz'],
            'qdId': lesson['qdId'],
            'isFz': lesson['isFz'],
            'fzMc': lesson['fzMc']
        }
        res = session.post(url, data=data, headers=http_header)
        if res.status_code != 200:
            raise Exception('get Checkin info failed')
        res = json.loads(res.text)
        return res['Rows']
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Get checkin info failed"
        }, indent=4))
        raise

def checkin(session, http_header, userInfo, lesson, tips=True):
    checkinInfo = getCheckinInfo(session, http_header, userInfo, lesson)
    print('签到口令：', checkinInfo['klHm'])
    # print(lesson['xsQdQk'], lesson['skXs'], lesson['bqMode'], lesson['qdNum'])
    if tips:
        if lesson['xsQdQk'] != '0' and lesson['skXs'] == '2' and (lesson['bqMode'] != '2' or lesson['qdNum'] != 1):
            choice = input('您似乎已经线下签到过了，是否继续签到？（y/n）')
            if choice != 'y':
                return
        if input('是否进行自动签到？（y/n）') != 'y':
            return
    try:
        url = serverUrl + "/saveXsQdInfo"
        data = {
            'sign': userInfo['sign'],
            'unitCode': userInfo['unitCode'],
            'userCode': userInfo['userCode'],
            'userName': userInfo['userName'],
            'bjMc': userInfo['bj'],
            'zyMc': userInfo['zy'],
            'xyMc': userInfo['xy'],
            'wzJd': str(float(checkinInfo['wzJd']) + (random.random() - 0.5) * 2 * 0.0001),
            'wzWd': str(float(checkinInfo['wzWd']) + (random.random() - 0.5) * 2 * 0.0001),
            'qdId': checkinInfo['uniqueCode'],
            'xkKh': checkinInfo['xkKh'],
            'skDd': lesson['skDd'],
            'xqj': lesson['xqj'],
            'djj': lesson['djj'],
            'djz': lesson['djz'],
            'isFace': None,
            # 'isFace': checkinInfo['xsIsFace'],
            'wzAcc': 0,
            'bqMode': lesson['bqMode'],
            'isFz': checkinInfo['isFz'],
            'fzMc': lesson['fzMc'],
            'djc': lesson['djc'],
            'qdJc': lesson['qdJc']
        }
        # print("**********")
        res = session.post(url, data=data, headers=http_header).text
        res = json.loads(res)
        if res['status'] == 1:
            print('签到成功！')
            return True
        elif res['status'] == 6:
            print('签到异常提醒：', res['msg'])
            return False
        else:
            print('签到失败！', res['msg'])
            raise Exception('签到失败：' + res['msg'])
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Checkin failed"
        }, indent=4))
        return False

def courseCheckin(session, http_header, userInfo):
    lesson = printCheckinList(session, http_header, userInfo, today=True)
    checkin(session, http_header, userInfo, lesson)

def autoCheckin(session, http_header, userInfo):
    print('自动签到检测已启动！')
    while True:
        try:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            print('正在检测签到列表...')
            lessons = getCheckinList(session, http_header, userInfo, today=False)
            flag_fail = False
            flag_success = False
            for lesson in lessons:
                if (lesson['qdQk'] == '1' and lesson['xsQdQk'] == '0') or (lesson['qdQk'] != '0' and lesson['bqMode'] == '2' and lesson['qdNum'] == 1):
                    print('正在自动签到：', lesson['kcMc'])
                    if checkin(session, http_header, userInfo, lesson, tips=False):
                        print('自动签到成功！')
                        flag_success = True
                    else:
                        print('自动签到失败！')
                        flag_fail = True
            # print('当前没有需要自动签到的课程，或者签到失败，10分钟后重新检测')
            if flag_fail:
                print('签到失败，1分钟后重新检测')
                time.sleep(60)
            elif not flag_success:
                print('当前没有需要自动签到的课程，10分钟后重新检测')
                time.sleep(600)
        except:
            print('自动签到检测出现异常，1分钟后重新检测')
            time.sleep(60)
