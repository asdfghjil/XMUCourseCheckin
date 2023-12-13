# 厦门大学课程自动签到脚本

大家好，这是小鸾写的一个勉强能用的用于应对厦门大学的课程签到的脚本，实现了以下功能：

- [x] 在远程伪装「线下」签到
- [x] 模拟扫描签到码签到
- [x] 定时扫描课程列表并自动签到
- [x] 查询一个老师的所有课程
- [x] 查询任意学生的课程列表和出勤记录
- [x] 查询学生出勤举报记录（举报功能已下线）

请注意，此脚本是小鸾用于学习 Python 语法和 `requests` 库的使用的，请勿用于其他非正当用途。

~~抵制无效学习，从我做起！~~

## 使用方法

### 准备抓包工具

首先，你需要准备一个可以抓 https 包的软件，这里推荐 [Fiddler Everywhere](https://www.telerik.com/fiddler/fiddler-everywhere)（付费）。如果你不想付费，推荐使用 [Proxyman](https://proxyman.io)。

在安装抓包工具后，你可能需要安装安装代理帮助程序工具、信任证书。以 Proxyman 为例，安装代理帮助程序工具会在第一次打开时自动提示安装，而若要信任证书，你应该点击标签栏「证书——在这台 Windows/Mac 上安装证书」，然后根据提示操作。

在需要查看 https 包内容时，右下角的「Response」页面中应该会提示「此 HTTPS 响应已加密，启用 SSL 代理以查看内容」。你应该选择「只对此域名启用」来查看这个 HTTPS 包的内容。

### 抓取 UserInfo

首先，将抓包工具挂在后台。

然后，请在你的计算机上打开微信，并进入「厦门大学智慧教务」小程序。

此时，请你回到你的抓包工具，找到对于 URL 「https://tingke.xmu.edu.cn/app/getUserOpenId」 的一条 POST 包。（如果你没有发现这一个记录，可以尝试进入小程序的「课程签到」页面再回来）

找到这一个包的响应内容。以 Proxyman 为例，你应该在右下角的 Response 中（可能需要点击启用 SSL 代理），打开 `Body` 页面。

其内容应该和下面的 JSON 类似：

```jsonc
{
  "msg": "openid获取成功",
  "userBindInfo": {
    "xy": "xx学院",     // 应该是你的学院
    "xz": "0",         // 应该是你的学制
    "bzrBmMc": "",
    "xsCc": "1",
    "openId": "o98y7tgUYKHLIUHGY23rasdf-asg",
    "bj": "null",
    "sign": "1234567890ABCDEF1234567",
    "isZj": "0",
    "dqz": 0,
    "isRoom": "0",
    "userCode": "xxxxxxxxxxxxxx",   // 应该是你的学号
    "avatarImgUrl": "head_img.png",
    "jzGx": "1",
    "uniqueCode": 123456,   // 应该是一串六位数字
    "roleCode": "0",
    "unitCode": "12345",    // 应该是一串五位数字
    "isTtk": "0",
    "isGl": "0",
    "sessionKey": "0",
    "unitName": "厦门大学",
    "isBind": "1",
    "isDs": "0",
    "xsXm": "顾小桑",  // 应该是你的名字
    "xsLb": "1",
    "xb": "null",
    "isNew": "0",
    "isBzr": "0",
    "userName": "顾小桑",   // 应该是你的名字
    "msBmMc": "",
    "xsXh": "xxxxxxxxxxxxxx",   // 应该是你的学号
    "roleName": "",
    "isJxMs": "0",
    "userType": "1",
    "isHk": "0",
    "nj": "2010",       // 应该是你的入学年份
    "isDel": "0",
    "xsXb": "1",
    "zy": "xxxxxxxx"    // 应该是你的专业名
  },
  "openId": "o98y7tgUYKHLIUHGY23rasdf-asg",
  "status": 1
}
```

### 下载项目并将学生信息保存 `userInfo.json`

你可以使用 `git clone` 或者在项目主页进行 Download Zip 下载本项目。

下载完成后，请在这个项目的根目录新建一个空文件，命名为 `userInfo.json`。

在你刚刚捕获到的 `json` 中，找到 `userBindInfo` 这一个条目。

请将这一条目的值，原封不动地保存进 `userInfo.json`。

如下所示：

```jsonc
// userInfo.json
{
    "xy": "xx学院",     // 应该是你的学院
    "xz": "0",         // 应该是你的学制
    "bzrBmMc": "",
    "xsCc": "1",
    "openId": "o98y7tgUYKHLIUHGY23rasdf-asg",
    "bj": "null",
    "sign": "1234567890ABCDEF1234567",
    "isZj": "0",
    "dqz": 0,
    "isRoom": "0",
    "userCode": "xxxxxxxxxxxxxx",   // 应该是你的学号
    "avatarImgUrl": "head_img.png",
    "jzGx": "1",
    "uniqueCode": 123456,   // 应该是一串六位数字
    "roleCode": "0",
    "unitCode": "12345",    // 应该是一串五位数字
    "isTtk": "0",
    "isGl": "0",
    "sessionKey": "0",
    "unitName": "厦门大学",
    "isBind": "1",
    "isDs": "0",
    "xsXm": "顾小桑",  // 应该是你的名字
    "xsLb": "1",
    "xb": "null",
    "isNew": "0",
    "isBzr": "0",
    "userName": "顾小桑",   // 应该是你的名字
    "msBmMc": "",
    "xsXh": "xxxxxxxxxxxxxx",   // 应该是你的学号
    "roleName": "",
    "isJxMs": "0",
    "userType": "1",
    "isHk": "0",
    "nj": "2010",       // 应该是你的入学年份
    "isDel": "0",
    "xsXb": "1",
    "zy": "xxxxxxxx"    // 应该是你的专业名
}
```

### 安装依赖

此脚本仅依赖于 `requests` 库，因此你只需要安装 `requests` 即可运行：

```shell
pip3 install requests
```

### 运行脚本

```shell
python3 app.py
```

运行脚本后，若你看到如下的内容即为正常。

```text
------------------ 小鸾的智慧教务 ------------------
1. 课程签到
2. 扫码签到
3. 课程自动签到
4. 课程查询
5. 学生出勤查询
6. 课程举报查询
0. 退出
```

### 自动签到

可以在此界面输入 3 进行定时扫描并自动签到。

请注意，由于个人主机和笔记本电脑的休眠机制，在休眠过程中自动签到不会运行，请勿在个人主机或笔记本上长时间运行自动签到，

如果需要长期定时自动签到，可以考虑使用云服务器等。

## 注意事项

1. 此脚本是小鸾用于学习 Python 语法和 `requests` 库的使用的，请勿用于其他非正当用途。
2. 如果打开「课程签到后」，不想对任何一门课签到，可以直接回车即可返回主界面。
3. 如果已经完成了线下签到，请勿重复使用此脚本签到。**后来的签到会自动覆盖之前的签到记录，因此可能会导致你的正常签到结果变成迟到！！！！！**
4. 当你使用「课程签到」时，「智慧教务」小程序服务端会根据当前的时间判断你的签到结果。如果你是正常时间（指在使用小程序签到时，能够得到「已签（线下）」这一结果的时间段），那么你的签到结果会是「已签」，否则你的签到结果会是「迟到」。这个「迟到」的结果不受签到结束的限制，也就是说，你在签到发起后当天的任何时间都可以进行签到，只是太迟会签成「迟到」。
5. 当你使用「扫码签到」时，只能在老师设置的签到时间段内签到，但是在此期间，一定可以获得「已签」的结果，不会出现「迟到」。
6. 还有更多功能待你挖掘o(￣▽￣)ｄ
