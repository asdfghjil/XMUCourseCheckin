import json
import requests
import sys

serverUrl = "https://tingke.xmu.edu.cn/app"
serverImg = "https://tingke.xmu.edu.cn/uploadFile"
serverIcon = "https://tingke.xmu.edu.cn/images/icon"
serverPhoto = "https://tingke.xmu.edu.cn/photo"
serverPdf = "https://tingke.xmu.edu.cn/pdf/"

userInfo = json.load(open("userInfo.json", "r", encoding="utf-8"))

# print(userInfo)

http_header = {
    "Host": "tingke.xmu.edu.cn",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac",
    "Content-Length": "126",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9"
}

session = requests.Session()

from checkin import courseCheckin, autoCheckin
from checkinScanCode import scanCheckin
from courseQuery import courseQuery
from attendanceQuery import attendanceQuery
from courseReportQuery import CourseReportQuery

while True:
    print('')
    print('------------------ 小鸾的智慧教务 ------------------')
    print('1. 课程签到')
    print('2. 扫码签到')
    print('3. 课程自动签到')
    print('4. 课程查询')
    print('5. 学生出勤查询')
    print('6. 课程举报查询')
    print('0. 退出')

    try:
        choice = int(input('请选择：'))
        if choice < 0 or choice > 6:
            raise Exception
    except:
        print('输入错误，请重新输入')
        continue
    try:
        if choice == 0:
            break
        if choice == 1:
            courseCheckin(session, http_header, userInfo)
        elif choice == 2:
            scanCheckin(session, http_header, userInfo)
        elif choice == 3:
            autoCheckin(session, http_header, userInfo)
        elif choice == 4:
            courseQuery(session, http_header, userInfo)
        elif choice == 5:
            attendanceQuery(session, http_header, userInfo)
        elif choice == 6:
            CourseReportQuery(session, http_header, userInfo)
    except:
        continue
