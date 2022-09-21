#flask, pymongo, dnspython,requests, bs4 일단 이렇게만 했습니다.
import certifi
from pymongo import MongoClient
from bs4 import BeautifulSoup
import hashlib
import datetime
import jwt
import requests
# import imp
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "../static/profile_pics"
SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://test:sparta@cluster0.287qhkj.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

# 로그인 여부 확인
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('main.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))



# HTML 화면 보여주기
@app.route('/')
def main():
    return render_template('main.html')

# 로그인 페이지
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=["POST"])
def sign_in():
    # form 타입으로 요청받은 username,password_give를 변수에 저장함
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # hash라이브러리의 sha256알고리즘으로 hexdigest함수를 이용하여 pw_hash 변수에 암호화 시킴
    # db에서 일치하는 아이디와 비밀번호를 찾아 result 변수에 저장
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one(
        {'username': username_receive, 'password': pw_hash})
    print(result)
    # 결과 값이 있으면 payload에 id와 유효시간을 저장함
    # token을 SECRET_KEY로 암호화 해줌 / 토큰에는 payload, SECRET_KEY, algorithm이 저장됨
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 4)  # 로그인 4시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    
    # 결과 값을 없으면 결과는 실패, msg를 json형식으로 보내줌
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 회원가입 페이지
@app.route('/sign_up')
def sign_up_page():
    return render_template('sign_up.html')

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

# 아이디 중복 검사
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})



@app.route("/list", methods=["POST"])
def game_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title': title,
        'image': image,
        'comment': comment_receive
    }
    db.list.insert_one(doc)

    return jsonify({'msg': '채널 추천 완료!'})


@app.route("/list", methods=["GET"])
def youtube_get():
    youtube_list = list(db.list.find({}, {'_id': False}))
    return jsonify({'youtube_list': youtube_list})


@app.route('/comment')
def comment():
    return render_template('comment.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
