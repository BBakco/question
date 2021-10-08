from flask import Flask, render_template, request, jsonify #, session
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbbbackco

app = Flask(__name__)


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

@app.route('/contents')
def contents():
    return render_template('contents.html')

@app.route('/userinfo')
def userinfo():
    return render_template('userinfo.html')


# API 역할을 하는 부분
# mainpage - section 2
@app.route('/get', methods=['GET'])
def home_get():
    home_question = list(db.contents.find({}, {'_id': False, 'question': 1}))
    home_answer = list(db.contents.find({}, {'_id': False, 'answer': 1}))

    return jsonify({'home_q': home_question, 'home_a': home_answer})


# contents
@app.route('/contents/get', methods=['GET'])
def contents_get():
    questions = list(db.questions_ko.find({}, {'_id': False}))

    return jsonify({'all_questions': questions})


@app.route('/contents/post', methods=['POST'])
def contents_post():
    question_receive = request.form['question_give']
    answer_receive = request.form['answer_give']

    # 시각 데이터로 원하는 문자열 만들기(한글일 경우)
    time_now = datetime.now()
    now_text = time_now.strftime("%Y{} %m{} %d{} %H{} %M{}")
    now_text = now_text.format('년', '월', '일', '시', '분')

    # db에 저장
    doc = {
        'question': question_receive,
        'answer': answer_receive,
        'time': now_text
    }
    db.contents.insert_one(doc)

    return jsonify({'msg': '답변이 저장되었습니다.'})


# mypage
@app.route('/mypage/get', methods=['GET'])
def read_answers():
    answers = list(db.contents.find({}, {'_id': False}))
    # answers = list(db.mypage_sample.find({'id': 'id1'}, {'_id': False}))
    return jsonify({'all_answers': answers})


# 정현님 로그인
@app.route('/login/post', methods=['GET', 'POST'])
def login():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']

    users = list(db.register.find({}, {'_id': False, 'email': 1, 'pw': 1}))

    emailli = []
    pwli = []
    for user in users:
        emailli.append(user['email'])
        pwli.append(user['pw'])

    if "@" and "." not in email_receive:
        return jsonify({"msg": "이메일을 확인해주세요"})
    elif not (email_receive and pw_receive):
        return jsonify({'msg': '패스워드를 입력해주세요'})
    else:
        # for user in users:
        if email_receive in emailli and pw_receive in pwli:
            return jsonify({'msg': '환영합니다'})
        else:
            return jsonify({'msg': '입력값을 확인하세요'})



# register
@app.route('/register', methods=['POST'])
def register_info():
    username_receive = request.form['username_give']
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    repeatpw_receive = request.form['repeatpw_give']

    if "@" not in email_receive:
        return jsonify({'msg': '이메일을 입력해주세요.'})

    elif '.' not in email_receive:
        return jsonify({'msg': '이메일을 완성해주세요'})

    elif not (email_receive and pw_receive and repeatpw_receive):
        return jsonify({'msg': '모두 입력해주세요'})

    doc = {
        'username': username_receive,
        'email': email_receive,
        'pw': pw_receive,
        'repeatpw': repeatpw_receive
    }

    db.register.insert_one(doc)
    return jsonify({'msg': '회원가입 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
