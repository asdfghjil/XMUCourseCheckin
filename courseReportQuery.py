import json
import requests
import sys

serverUrl = "https://tingke.xmu.edu.cn/app"

from checkinList import printCheckinList

def getCourseReportData(session, http_header, userInfo, qdId):
    try:
        url = serverUrl + "/getQdYcXsList"
        data = {
            'sign': userInfo['sign'],
            'userType': userInfo['userType'],
            'userCode': userInfo['userCode'],
            'unitCode': userInfo['unitCode'],
            'qdId': qdId
        }
        res = session.post(url, data=data, headers=http_header)
        if res.status_code != 200:
            raise Exception('Get course report data failed')
        res = json.loads(res.text)
        return res['Rows']
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Get course report data failed"
        }, indent=4))
        raise

def CourseReportQuery(session, http_header, userInfo):
    qdId = printCheckinList(session, http_header, userInfo, type="查询")['qdId']
    data = getCourseReportData(session, http_header, userInfo, qdId)
    print('')
    if len(data) == 0:
        print('您的同学团结友爱，没有举报情况！')
    else:
        print('举报总数：', len(data), ":")
    for id, stu in enumerate(data):
        print(str(id) + ".", stu['xsXm'], stu['xsXh'], stu['xsQdSj'], stu['jbYyXm'])