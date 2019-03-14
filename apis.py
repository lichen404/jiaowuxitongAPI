import hashlib
import requests
import html
import lxml.html
import logging
from urllib import parse
from flask import jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s  - %(message)s')
logger = logging.getLogger(__name__)
url = 'http://123.15.36.138:8008/zfmobile_port/webservice/jw/EducationalPortXMLService'
header = {
    'User-Agent': 'KSOAP/2.0',
    'HOST': '123.15.36.138:8008',
    'Content-Type': 'text/xml',
   
}


# 创建response类
class jsonResponse(object):
    def __init__(self, code, reason, result):
        self.code = code
        self.reason = reason
        self.result = result


# 把类先转换成dict，方便转成json
def class2dict(jresp):
    return {
        'code': jresp.code,
        'reason': jresp.reason,
        'result': jresp.result
    }


#  获取照片所需要的key可以在其他情况下复用
def getStuPhotoKey(stuID):
    RawKey = hashlib.md5(
        (stuID + 'DAFF8EA19E6BAC86E040007F01004EA').encode('utf8'))
    Key = (RawKey.hexdigest()).upper()

    return Key


def getStuInfoKey(stuID):
    return getStuPhotoKey(stuID)


def getStuCourseScheduleKey(stuID, year, term):
    RawKey = hashlib.md5((parse.quote(
        stuID + '&' + year + '&' + term + 'DAFF8EA19E6BAC86E040007F01004EA').encode('utf8')))
    Key = (RawKey.hexdigest()).upper()
    return Key


def getStuGradeScore(stuID, header):
    data = '<v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:d="http://www.w3.org/2001/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/" xmlns:v="http://schemas.xmlsoap.org/soap/envelope/"><v:Header /><v:Body><n0:GradeScoreInfoSearch id="o0" c:root="1" xmlns:n0="http://service.jw.com/"><sid i:type="d:string">{id}</sid><count i:type="d:string">0</count><strKey i:type="d:string">{key}</strKey></n0:GradeScoreInfoSearch></v:Body></v:Envelope>'
    data = data.format(id=stuID, key=getStuPhotoKey(stuID))
    try:
        urlhd = requests.post(url, headers=header, data=data.encode('utf-8'))

    except Exception as e:
        logger.info(e)

        resp = jsonResponse('404', 'Failed', ['学校服务器当前可能无法访问'])
        resp = class2dict(resp)
        return jsonify(resp)
    page = urlhd.text
    page = html.unescape(page)
    tree = lxml.html.etree.HTML(page)
    cetNode = tree.xpath("//ksmc")
    scoreNode = tree.xpath("//cj")
    cetTimeNode = tree.xpath("//xn")
    if cetNode:
        scoreList = []
        cetTimeList = []
        cetList = []
        for z in cetTimeNode:
            cetTimeList.append(z.text)
        for x in scoreNode:
            scoreList.append(x.text)
        for y in cetNode:
            cetList.append(y.text)
        dictList = []
        for x, y, z in zip(scoreList, cetTimeList, cetList):
            d = dict(name=z, time=y, score=x)
            dictList.append(d)
        resp = jsonResponse('200', 'Success', dictList)
        resp = class2dict(resp)
        return jsonify(resp)
    else:
        resp = jsonResponse('404', 'failed', ['请检查输入内容是否正确'])
        resp = class2dict(resp)
        return jsonify(resp)


def getStuScore(stuID, header):
    data = '<v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:d="http://www.w3.org/2001/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/" xmlns:v="http://schemas.xmlsoap.org/soap/envelope/"><v:Header /><v:Body><n0:ScoreSearch id="o0" c:root="1" xmlns:n0="http://service.jw.com/"><sid i:type="d:string">{id}</sid><count i:type="d:string">0</count><strKey i:type="d:string">{key}</strKey></n0:ScoreSearch></v:Body></v:Envelope>'
    data = data.format(id=stuID, key=getStuPhotoKey(stuID))
    try:
        urlhd = requests.post(url, headers=header, data=data.encode('utf-8'))
    except Exception as e:
        logger.info(e)
        resp = jsonResponse('404', 'Failed', ['学校服务器当前可能无法访问'])
        resp = class2dict(resp)
        return jsonify(resp)
    page = urlhd.text
    page = html.unescape(page)
    tree = lxml.html.etree.HTML(page)
    courseNodeList = tree.xpath("//kcmc")  # 课程名称
    scoreNodeList = tree.xpath("//zscj")  # 课程总成绩
    if scoreNodeList:
        # print(scoreNodeList)
        courseList = []
        scoreList = []
        for x in courseNodeList:
            courseList.append(x.text)
        for x in scoreNodeList:
            scoreList.append(x.text)
            tempList = zip(courseList, scoreList)
        dictList = []
        for x, y in tempList:
            d = dict(course=x, score=y)
            dictList.append(d)
        resp = jsonResponse('200', 'Success', dictList)
        resp = class2dict(resp)
        return jsonify(resp)
    else:
        resp = jsonResponse('404', 'failed', ['请检查输入内容是否正确'])
        resp = class2dict(resp)
        return jsonify(resp)


def getStuInfo(stuID, header):
    data = '<v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:d="http://www.w3.org/2001/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/" xmlns:v="http://schemas.xmlsoap.org/soap/envelope/"><v:Header /><v:Body><n0:StudentInfoSearch id="o0" c:root="1" xmlns:n0="http://service.jw.com/"><sid i:type="d:string">{id}</sid><count i:type="d:string">0</count><strKey i:type="d:string">{key}</strKey></n0:StudentInfoSearch></v:Body></v:Envelope>'
    data = data.format(id=stuID, key=getStuInfoKey(stuID))
    try:
        urlhd = requests.post(url, headers=header, data=data.encode('utf-8'))
    except Exception as e:
        logger.info(e)
        resp = jsonResponse('404', 'Failed', ['学校服务器当前可能无法访问'])
        resp = class2dict(resp)
        return jsonify(resp)
    page = urlhd.text
    page = html.unescape(page)
    tree = lxml.html.etree.HTML(page)
    keyList = []
    valueList = []
    key = tree.xpath("//name")
    value = tree.xpath("//value")
    for x in key:
        keyList.append(x.text)
    for x in value:
        valueList.append(x.text)
    dictList = dict(zip(keyList, valueList))
    resp = jsonResponse('200', 'Success', dictList)
    resp = class2dict(resp)
    # print(resp)

    return jsonify(resp)


def parseSchdeule(schedule):
    scheduleList = []
    for x in schedule:
        scheduleList.append(x.tail.strip())
    timeList = scheduleList[::3]
    teacherList = scheduleList[1::3]
    classroomList = scheduleList[2::3]
    tempList = zip(timeList, teacherList, classroomList)
    dictList = []
    for x, y, z in tempList:
        d = dict(time=x, teacher=y, classroom=z)
        dictList.append(d)
    # print(dictList)
    return dictList


def getStuCourseSchedule(stuID, schoolYear, term, header):
    data = '<v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:d="http://www.w3.org/2001/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/" xmlns:v="http://schemas.xmlsoap.org/soap/envelope/"><v:Header /><v:Body><n0:CourseScheduleSearch id="o0" c:root="1" xmlns:n0="http://service.jw.com/"><userName i:type="d:string">{id}</userName><year i:type="d:string">{year}</year><term i:type="d:string">{term}</term><role i:type="d:string">XS</role><count i:type="d:string">0</count><strKey i:type="d:string">{key}</strKey></n0:CourseScheduleSearch></v:Body></v:Envelope>'
    data = data.format(id=stuID, year=schoolYear, term=term, key=getStuCourseScheduleKey(stuID, schoolYear, term))
    try:
        urlhd = requests.post(url, headers=header, data=data.encode('utf-8'))
    except Exception as e:
        logger.info(e)
        resp = jsonResponse('404', 'Failed', ['学校服务器当前可能无法访问'])
        resp = class2dict(resp)
        return resp
    page = urlhd.content.decode("utf8")
    page = html.unescape(page)
    # print(page)
    tree = lxml.html.etree.HTML(page)
    courseNameList = []
    dayList = []
    weekList = []
    creditList = []
    classTimeList = []
    classroomList = []
    currentWeek = tree.xpath("//dqz")  # 当前周
    # print(currentWeek[0].text)
    if (currentWeek):
        timeNow = {'currentCourseWeek': currentWeek[0].text}
    else:
        timeNow = {'currentCourseWeek': None}
    courseNameNodeList = tree.xpath("//kcmc")  # 课程名称

    for x in courseNameNodeList:
        courseNameList.append(x.text)
    # print(courseList)
    day = tree.xpath("//xqj")  # 星期几上课
    for x in day:
        dayList.append(x.text)
    # print(dayList)
    classWeek = tree.xpath("//skz")  # 上课周
    for x in classWeek:
        weekList.append(x.text)
    # print(weekList)
    credit = tree.xpath("//xf")  # 学分
    for x in credit:
        creditList.append(x.text)
    # print(creditList)
    classroom = tree.xpath("//skjs")
    for x in classroom:
        classroomList.append(x.text)  # 上课教室

    classTime = tree.xpath("//js")  # 第几节上课
    for x in classTime:
        classTimeList.append(x.text)
    # print(classTimeList)
    courseList = zip(courseNameList, dayList, weekList, creditList, classroomList, classTimeList)
    dictList = []
    dictList.append(timeNow)
    for a, b, c, d, e, f in courseList:
        d = dict(courseName=a, day=b, classweek=c, credit=d, classroom=e, classTime=f)
        dictList.append(d)

    # test  print(dictList[0]['schedule']['teacher'])
    resp = jsonResponse('200', 'Success', dictList)

    resp = class2dict(resp)
    # print(resp)
    return jsonify(resp)


def getStuPhoto(stuID, header):
    data = '<v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:d="http://www.w3.org/2001/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/" xmlns:v="http://schemas.xmlsoap.org/soap/envelope/"><v:Header /><v:Body><n0:StudentPhotosSearch id="o0" c:root="1" xmlns:n0="http://service.jw.com/"><sid i:type="d:string">{id}</sid><strKey i:type="d:string">{key}</strKey></n0:StudentPhotosSearch></v:Body></v:Envelope>'
    data = data.format(id=stuID, key=getStuPhotoKey(stuID))
    try:
        Rawcontent = requests.post(url, data=data.encode('utf8'), headers=header)

    except Exception as e:
        logger.info(e)
        resp = jsonResponse('404', 'Failed', ['学校服务器当前可能无法访问'])
        resp = class2dict(resp)
        return jsonify(resp)

    content = Rawcontent.text
    tree = lxml.html.etree.HTML(content)
    element = tree.xpath('//return')
    if (element):
        strBase64Photo = element[0].text
        result = {'base64img': strBase64Photo}
        resp = jsonResponse('200', 'Success', result)
    else:
        pass

    resp = class2dict(resp)
    # print(json.loads(resp))
    return jsonify(resp)

# getStuCourseSchedule('201516010307','2017-2018','1',header)
