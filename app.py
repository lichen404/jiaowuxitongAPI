from flask import Flask, request
from flask_cors import CORS
import apis

app = Flask(__name__)
cors = CORS(app, resource={'/v1/GET/*': {"origin": "*"}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/v1/GET/stu_grade_score/<ID>', methods=['GET', 'POST'])
def gradeScore(ID):
    resp = apis.getStuGradeScore(ID, apis.header)
    return resp


@app.route('/v1/GET/stu_score/<ID>', methods=['GET', 'POST'])
def score(ID):
    resp = apis.getStuScore(ID, apis.header)
    return resp


@app.route('/v1/GET/stu_course_schedule/<ID>', methods=['GET', 'POST'])
def courseSchedule(ID):
    year = request.args.get('year')
    term = request.args.get('term')
    if year and term:
        schoolYear = year
        # schoolYear = str(year) + '-' + str(int(year) + 1)
        resp = apis.getStuCourseSchedule(ID, schoolYear=schoolYear, term=term, header=apis.header)
        return resp
    else:
        resp = apis.jsonResponse('404', 'failed', ['请检查输入内容是否正确'])
        resp = apis.class2dict(resp)
        # print(resp)
        return apis.jsonify(resp)


@app.route('/v1/GET/stu_photo/<ID>', methods=['GET', 'POST'])
def stuPhoto(ID):
    resp = apis.getStuPhoto(ID, apis.header)
    return resp


@app.route('/v1/GET/stu_info/<ID>', methods=['GET', 'POST'])
def stuInfo(ID):
    resp = apis.getStuInfo(ID, apis.header)
    return resp


@app.route('/v1/POST/stu_login_status', methods=['POST'])
def stuLoginStatus():
    print(request.form)
    stuID = request.form['stuID']
    stuPwd = request.form['stuPwd']
    resp = apis.getLoginState(stuID, stuPwd, apis.header)
    return resp


if __name__ == '__main__':
    app.run('0.0.0.0')
