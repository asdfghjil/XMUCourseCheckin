import json
import requests
import sys

serverUrl = "https://tingke.xmu.edu.cn/app"

def display(coursename, li):
    print(coursename, '：')
    for id, l in enumerate(li):
        print(id, l['qdRq'], f"第{l['djz']}周 星期{l['xqj']}: {l['qdQkStr']}({l['skXsStr']})")

def attendanceQuery(session, http_header, userInfo):
    try:
        name = input('请输入姓名或学号：')
        url = serverUrl + "/searchXsCqList"
        data = {
            'sign': userInfo['sign'],
            'userType': userInfo['userType'],
            'userCode': userInfo['userCode'],
            'unitCode': userInfo['unitCode'],
            'inputValue': name,
            'kcCc': '1'
        }
        res = session.post(url, data=data, headers=http_header)
        if res.status_code != 200:
            print('Get attendance query data info failed')
            return
        res = json.loads(res.text)
        if res['status'] != 1:
            print('Get attendance query data info failed')
            return
        info = res['Rows']
        print(name, '的出勤课程：')
        print('0 显示全部（刷屏警告）')
        for id, course in enumerate(info):
            print(id + 1, course['kcMc'], '\t', course['jsXm'])
        c_course = int(input('请输入查询的课程序号：'))
        if c_course < 0 or c_course > len(info):
            raise Exception('Invalid course')
        if c_course == 0:
            for id, course in enumerate(info):
                display(course['kcMc'] + ' ' + course['jsXm'], course['qdLi'])
        else:
            display(info[c_course - 1]['kcMc'] + ' ' + info[c_course - 1]['jsXm'], info[c_course - 1]['qdLi'])
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Get attendance query data info failed"
        }, indent=4))
        return