import json
import requests
import sys

serverUrl = "https://tingke.xmu.edu.cn/app"

def getCourseQueryDataInfo(session, http_header, userInfo):
    try:
        url = serverUrl + "/getLdPjList"
        data = {
            'sign': userInfo['sign'],
            'userType': userInfo['userType'],
            'userCode': userInfo['userCode'],
            'unitCode': userInfo['unitCode'],
            'bm': None,
            'key': None,
            'isSearch': 0,
            'kkXy': 'ALL',
            'djz': '',
            'xqj': '',
            'djj': '',
            'jsXm': ''
        }
        res = session.post(url, data=data, headers=http_header)
        if res.status_code != 200:
            raise Exception('Get course query data info failed')
        res = json.loads(res.text)
        return res['xyLi'], res['jxzLi'], res['ccLi']
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Get course query data info failed"
        }, indent=4))
        raise

def displayCourse(course, showall=True):
    if not showall:
        print(course['kcCcStr'], course['kcMc'], course['jsXm'], f'周{course["dxXqj"]}第{course["skSj"]}节' if course['dxXqj'] != '十' else '无固定上课时间', course['skDd'], course['kcZt'])
    else:
        print('课程层次：', course['kcCcName'])
        print('课程名称：', course['kcMc'])
        print('教师：', course['jsXm'], '联合授课' if course['isLhSk'] == '1' else '')
        print('上课日期：', course['curDate'])
        print('上课时间：', f'周{course["dxXqj"]}第{course["skSj"]}节' if course['dxXqj'] != '十' else '无固定上课时间')
        print('课程性质：', course['kcXz'], '实践课' if course['isSxKc'] == '1' else '', '实验课' if course['isSyKc'] == '1' else '', '线上课' if course['isXsKc'] == '1' else '')
        print('授课学院：', course['kkXy'])
        print('上课地点：' if course['isSyKc'] != '1' else '实验地点', course['skDd'], f"({course['xqMc']})")
        print('上课人数：', course['yxRs'], '人')
        print('课程状态：', course['kcZt'])
        print('考勤情况：', '未发起考勤' if course['isQd'] == '0' else f"总{course['kcRs']}人 出勤{course['qdNum']}/迟到{course['cdRs']}/请假{course['qjRs']}/出勤率{course['cqLv']}%" if course['isQd'] == '1'  else '只提供当天记录')

def courseQuery(session, http_header, userInfo):
    try:
        schools, weeks, levels = getCourseQueryDataInfo(session, http_header, userInfo)
        print('课程层次：')
        for id, level in enumerate(levels):
            print(id, level['dicName'])
        c_level = int(input('请输入课程层次：'))
        if c_level < 0 or c_level >= len(levels):
            raise Exception('Invalid level')
        print('学院：')
        for id, school in enumerate(schools):
            print(id, school['c1'], end='\n' if id % 7 == 6 or id == len(schools) - 1 else '\t')
        c_school = int(input('请输入学院：'))
        if c_school < 0 or c_school >= len(schools):
            raise Exception('Invalid school')
        print('周次：')
        for id, week in enumerate(weeks):
            print(id, week['c2'], end='\n' if id % 5 == 4 or id == len(weeks) - 1 else '\t')
        c_week = int(input('请输入周次：'))
        if c_week < 0 or c_week >= len(weeks):
            raise Exception('Invalid week')
        name = input('请输入教师姓名：')

        key = schools[c_school]['c1'] + "|" + weeks[c_week]['c1'] + "|" + name

        url = serverUrl + "/getSearchKcKbList"
        data = {
            'sign': userInfo['sign'],
            'userType': userInfo['userType'],
            'userCode': userInfo['userCode'],
            'unitCode': userInfo['unitCode'],
            'inputValue': key,
            'isToday': 0,
            'type': 5,
            'djj': '',
            'skcd': '',
            'xqj': '',
            'curXq': '',
            'curXqInt': '',
            'kcCc': levels[c_level]['dicCode']
        }
        res = session.post(url, data=data, headers=http_header)
        if res.status_code != 200:
            print('course query failed')
            return
        res = json.loads(res.text)
        courses = res['Rows']
        print("查询结果：")
        for id, course in enumerate(courses):
            print(id)
            displayCourse(course)
            
    except:
        print(json.dumps({
            "status": "failed",
            "reason": "Invalid input",
        }, indent=4))
        return