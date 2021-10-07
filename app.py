from flask import Flask, render_template, request, jsonify #, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime #, timedelta

client = MongoClient('localhost', 27017)
db = client.dbbbackco

app = Flask(__name__)
# app.secret_key = "BBackco@question!"
# app.permanent_session_lifetime = timedelta(days=1)


# HTML 화면 보여주기
@app.route('/')
def home():
    # if 'username' in session:
    #     username = session['username']
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

    return jsonify({'msg': '저장되었습니다.'})


# mypage
@app.route('/mypage/get', methods=['GET'])
def read_answers():
    answers = list(db.mypage_sample.find({'id': 'id1'}, {'_id': False}))
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


# # 로그인 이용자 확인 처리
# @app.route('/home#pop1', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('mainpage.html')
#     else:
#         id = request.form['id']
#         pw = request.form['pw']
#         # id와 pw 검사
#         if "@" and "." not in email_receive:
#             email_receive = request.form['email_give']
#             pw_receive = request.form['pw_give']
#             session['user'] = id
#             return redirect(url_for('login'))
#         else:
#             session['logFlag'] = True
#             session['username'] = username
#             return render_template('session_view.html')
#     else:
#     return jsonify({"msg": '아이디 또는 패스워드를 확인 하세요.'})
#
#
# # Login Sever
# @app.route('/home#pop1', methods=['POST'])
# def sign_in():
#     email_receive = request.form['email_give']
#     pw_receive = request.form['pw_give']
#
#     result = db.register.find_one({'username': email_receive, 'password': pw_receive})
#     if result is not None:
#         payload = {'id': email_receive, 'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)}
#         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
#         return jsonify({'result': 'success', 'token': token})
#     # 찾지 못하면
#     else: return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
#
#
# @app.route("/logout")
# def logout():
#     session.pop('user', None)
#     return jsonify({'msg': '로그아웃 하시겠습니까?'})


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
