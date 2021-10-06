from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.dbbbackco
app = Flask(__name__)


# HTML 화면 보여주기
@app.route('/home')
def home():
    return render_template('mainpage.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


@app.route('/contents')
def contents():
    return render_template('contents.html')


# API 역할을 하는 부분
# mainpage - section 2
@app.route('/home/get', methods=['GET'])
def home_get():
    home_question = list(db.contents.find({}, {'_id': False, 'question': 1}))
    home_answer = list(db.contents.find({}, {'_id': False, 'answer': 1}))

    return jsonify({'home_q': home_question,'home_a': home_answer})


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
    answers = list(db.mypage_sample.find({'id':'id1'}, {'_id': False}))
    return jsonify({'all_answers': answers})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
