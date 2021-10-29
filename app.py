from flask import Flask, render_template, request, jsonify, session, redirect, flash
import pymongo
from pymongo import MongoClient
from datetime import datetime
from functools import wraps
import re
from flask.json import jsonify

# models.py에서 추가로 import 필요한 것들.
# from passlib.hash import pbkdf2_sha256
import hashlib
import uuid
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

# werkzeug.security :이걸로 비밀번호 암호화

# routes.py에서 추가로 Import(할게 없었다)

app = Flask(__name__)
app.secret_key = b'\xd79\x91@\x87\nM\x85=\xb0QL\n\xd5b('

# db 이름이랑, 이하 collection이름들을 영선님 파일에 맞추어야 할 것
client = MongoClient('mongodb://bbackco:Qkrzh2ndp@13.209.20.75', 27017)
db = client.dbbbackco


# 데코레이터 - 로그인 할 경우만 들어갈 수 있음
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/')

    return wrap


# HTML 화면 보여주기
@app.route('/')
def home():
    if not session:
        return render_template('mainpage.html')
    else:
        return render_template('mainpage_after.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/mypage')
@login_required
def mypage():
    return render_template('mypage.html')


@app.route('/contents')
@login_required
def contents():
    return render_template('contents.html')


@app.route('/userinfo')
@login_required
def userinfo():
    return render_template('userinfo.html')


@app.route('/search')
def search():
    return render_template('search.html')


# admin 페이지
@app.route('/bbackcoadminbback')
def admin():
    return render_template('admin2.html')


# 로그인 한 후에 보이는 메인페이지
@app.route('/main/user')
@login_required
def afterlogin():
    return render_template('mainpage_after.html')


# 세션상태 확인하는 곳
@app.route('/session')
def checksession():
    return render_template('session_view.html')


# db랑 연결되어서 get, post하는 부분
# API 역할을 하는 부분
# mainpage - section 2
@app.route('/get', methods=['GET'])
def home_get():
    home_question = list(db.contents.find({}, {'_id': False, 'question': 1}).sort('like', pymongo.DESCENDING))
    home_answer = list(db.contents.find({}, {'_id': False, 'answer': 1}).sort('like', pymongo.DESCENDING))
    home_article_id = list(db.contents.find({}, {'_id': 1}).sort('like', pymongo.DESCENDING))
    home_likes = list(db.contents.find({}, {'like': 1}).sort('like', pymongo.DESCENDING))
    home_img = list(db.contents.find({}, {'img': 1}).sort('like', pymongo.DESCENDING))
    return jsonify(
        {'home_q': home_question, 'home_a': home_answer, 'home_id_atc': home_article_id, 'home_like': home_likes,
         'home_img': home_img})


# contents
@app.route('/contents/get', methods=['GET'])
def contents_get():
    questions = list(db.questions_ko.find({}, {'_id': False}))

    return jsonify({'all_questions': questions})


# contents에서 글을 post하는 부분.
@app.route('/contents/post', methods=['POST'])
def contents_post():
    # user_receive = request.form['user_give']
    question_receive = request.form['question_give']
    answer_receive = request.form['answer_give']
    # 이 아래 writer가 세션에 들어가 있는 현재 사용자의 email 정보를 받아오는 변수
    writer = session['user']['email']
    # print(writer)
    # img = db.contents.find({'user':session['user']['email']}, {'img':1, '_id':0})['img']
    img = db.users.find_one({'email': session['user']['email']}, {'img': 1})
    img = img['img']
    print(img)

    # 시각 데이터로 원하는 문자열 만들기(한글일 경우)
    time_now = datetime.now()
    now_text = time_now.strftime("%Y{} %m{} %d{} %H{} %M{}")
    now_text = now_text.format('년', '월', '일', '시', '분')

    # db에 저장
    doc = {
        # 'user': session['user']['email'],
        "_id": uuid.uuid4().hex,  # 고유 식별자 만들어주는 거
        'question': question_receive,
        'answer': answer_receive,
        'time': now_text,
        'user': writer,
        'like': 0,
        'img': img
    }

    db.contents.insert_one(doc)

    return jsonify({'msg': '답변이 저장되었습니다.'})


# mypage
# 여기서 db에서 contents 콜렉션에서 'user'키에 해당하는 값이 현재 세션의 email 정보와 동일할 경우에만 자료를 가져옴.
@app.route('/mypage/get', methods=['GET'])
def read_answers():
    answers = list(db.contents.find({'user': session['user']['email']}, {'_id': False}))
    # answers = list(db.mypage_sample.find({'id': 'id1'}, {'_id': False}))
    return jsonify({'all_answers': answers})


# 내가 공감한 글 모아보기
# @app.route('mypage/liked-get', methods=['GET'])
# def collectArticlesLiked():
#     articles = db.users.find({'email':session['user']['email']},{})


# search페이지 처음에 GET 띄우기
@app.route('/search/get', methods=['GET'])
def browse():
    answer_li = list()
    docs = db.contents.find({}).sort('time', pymongo.DESCENDING).limit(39)

    for doc in docs:
        answer_li.append(doc)
    results = answer_li
    return jsonify({'all_results': results})

    # return render_template('search.html', results = results, range = '모든 글', keyword = '')


# 키워드 검색 페이지
@app.route('/keyword/search', methods=['POST'])
def keywordsearch():
    contents = db.contents
    answer_li = list()
    word = request.form.get('keyword')
    scope = request.form.get('scope')
    standard = request.form.get('align-standard')

    if scope == 'all':
        docs = contents.find({'$or': [{'answer': {'$regex': word}}, {'question': {'$regex': word}}]},
                             {'_id': 1, 'question': 1, 'answer': 1, 'like': 1, 'img': 1})
        if standard == 'recent':
            docs.sort('time', pymongo.DESCENDING)
            for doc in docs:
                answer_li.append(doc)
            results = answer_li
            return render_template('search.html', results=results, range='모든 글', keyword=word, criterion='recent')
        elif standard == 'like':
            docs.sort('like', pymongo.DESCENDING)
            for doc in docs:
                answer_li.append(doc)
            results = answer_li
            return render_template('search.html', results=results, range='모든 글', keyword=word, criterion='like')
        elif not standard:
            flash("정렬기준을 선택해주세요")
            return render_template('search.html')
    elif scope == 'useronly':
        docs = contents.find(
            {'user': session['user']['email'], '$or': [{'answer': {'$regex': word}}, {'question': {'$regex': word}}]},
            {'_id': 1, 'question': 1, 'answer': 1, 'like': 1, 'img': 1})
        if standard == 'recent':
            docs.sort('time', pymongo.DESCENDING)
            for doc in docs:
                answer_li.append(doc)
            results = answer_li
            return render_template('search.html', results=results, range='나의 글', keyword=word, criterion='recent')
        elif standard == 'like':
            docs.sort('like', pymongo.DESCENDING)
            for doc in docs:
                answer_li.append(doc)
            results = answer_li
            return render_template('search.html', results=results, range='나의 글', keyword=word, criterion='like')
        elif not standard:
            flash("정렬기준을 선택해주세요")
            return render_template('search.html')
    elif not scope and not standard:
        flash("검색 범위와 정렬 기준을 선택해주세요")
        return render_template('search.html')
    elif not scope:
        flash("검색 범위를 선택해주세요")
        return render_template('search.html')


# 검색페이지에서 좋아요 기능
@app.route('/like', methods=['POST'])
def like():
    if session:
        contents = db.contents
        article_id_receive = request.form['article_id_give']
        target = contents.find_one({'_id': article_id_receive}, {'_id': 1})
        # print(target)

        already_liked = db.users.find_one({'email': session['user']['email']}, {'article-liked': 1, '_id': 0})
        already_liked_list = already_liked['article-liked']

        current_like = contents.find_one({'_id': article_id_receive})['like']
        # print(current_like)
        new_like = current_like + 1

        # target_without_like = contents.find_one({'_id':article_id_receive}, {'like':0})
        # # print(already_liked_list)

        if target in already_liked_list:
            return jsonify({'msg': '이미 공감한 글입니다.'})
        else:
            already_liked_list.append(target)
            db.users.update_one({'email': session['user']['email']}, {'$set': {'article-liked': already_liked_list}})
            contents.update_one({'_id': article_id_receive}, {'$set': {'like': new_like}})
            return jsonify({'msg': '공감 완료!'})
    else:
        return jsonify({'msg': '로그인 후 공감부탁드려요😄'})


# 이하  models.py 부분
# User 클래스 만들고 여러 메소드들
class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        flash("환영합니다!")
        return render_template('mainpage_after.html')

    # flash 띄울 때 '00님'부르도록 하자

    def signup(self):
        # print(request.form)

        # user객체 생성하기
        user = {
            "_id": uuid.uuid4().hex,  # 고유 식별자 만들어주는 거
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "article-liked": [],
            "img": request.form.get('img-select')
        }

        myimg = user['img']
        # print(myimg)

        # password 암호화(encryption) -- 여러 시도들
        # user['password'] = pbkdf2_sha256.hash(user['password'])
        # user['password'] = hashlib.sha256(user['password'].encode())
        user['password'] = generate_password_hash(user['password'])

        # 이미 존재하는 email인지 확인하기
        if db.users.find_one({"email": user['email']}):
            # return jsonify({"error": "이메일 주소가 이미 사용중입니다."}), 400
            flash("이메일 주소가 이미 사용중입니다.")
            return render_template('register.html');
        elif db.users.insert_one(user):
            # flash("회원가입 완료! 환영합니다!")
            return self.start_session(user);
        else:
            return jsonify({"error": "Signup failed"}), 400;

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })
        # 패스워드도 확인하는 절차 : 앞에 암호화된 부분, 뒤에를 암호화 안 된 입력값으로 넣어야 되더라는!(순서 중요)
        if user and check_password_hash(user['password'], request.form.get('password')):
            return self.start_session(user);
            # print(session["logged_in"]);
        return jsonify({"error": "가입되어 있지 않은 이메일입니다."}), 401


# 회원가입, 로그아웃(signout), 로그인에 대한 routes.
# routes.py
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route('/user/signout')
def signout():
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)