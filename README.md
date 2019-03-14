## 河南工业大学移动教务API集合
一个使用Python flask在移动教务APP的基础上二次开发的API集合，正常运行依赖学校服务器的稳定
****

### feature
* 使用更加简洁方便的json替换XML传输数据
* 修改了原API中不易理解的使用拼音的键名，如djz（第几周），skjs（上课教室）等
* 采用RESTful风格的API设计

### Usage
请求示例：http://apis.stayw1thme.xyz/v1/GET/stu_score/学号  

请求方式：get  

返回格式：json

stu_score为可替换项，返回结果为该学号学生所有课程成绩。可替换为如下参数：


|Keywords|means|extra|
|----|----|----|
|stu_grade_score|英语四六级成绩及大学英语成绩| |
|stu_course_schedule|学生课程|需要额外GET参数year(学年，示例：2018)和term（学期，示例：1）|
|stu_photo|学生教务系统照片|返回照片结果为base64编码格式| |
|stu_info|学生相关学籍信息| |

	JSON返回示例：
```javascript
{"code": "200",
 "reason": "Success", 
 "result": [{
 	"currentCourseWeek": null},               //当前上课周，因为现在是假期，所以为空。
{"courseName": "信息安全概论",
 "day": "4",                                //星期四
 "classweek": "4,5,6,7,8,9,10,11,12,13,14", //上课周
 "credit": "3.0",                           //课程学分
 "classroom": "莲4号教学楼506",              //上课教室
 "classTime": "3,4"},                      //上课节数
 {"courseName": "信息安全概论",
 "day": "1",
 "classweek": "4,5,6,7,8,9,10,11,12,13,14", 
 "credit": "3.0",
 "classroom": "莲4号教学楼506", "classTime": "3,4"},
 ]}


```
###Demo
四六级成绩查询:[https://dl.stayw1thme.xyz/demo.html](https://dl.stayw1thme.xyz/demo.html)
