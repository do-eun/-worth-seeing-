#flask, pymongo, dnspython,requests, bs4 일단 이렇게만 했습니다.
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
client = MongoClient('mongodb+srv://test:sparta@cluster0.znplsth.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def main():
    return render_template('list.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/list", methods=["POST"])
def channel_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    video_receive = request.form['video_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title':title,
        'image':image,
        'comment':comment_receive,
        'video': video_receive
    }
    db.list.insert_one(doc)

    return jsonify({'msg':'채널 추천 완료!'})

@app.route("/list", methods=["GET"])
def youtube_get():
    youtube_list = list(db.list.find({}, {'_id':False}))
    return jsonify({'youtube_list': youtube_list})

@app.route('/comment')
def comment():
    return render_template('comment.html')

# 진자2로 db에서 프로필 값 보내주기인데 확실하지 않아요..안되면 프로필 빼고 가는걸로..
# @app.route('/comment')
# def comment():
#     profile = list(db.worthseeing.find({}, {"_id": False}))
#     return render_template('index.html', profile=profile)

# 코멘트 db 저장
@app.route("/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']

    doc = {
        'comment': comment_receive
    }
    db.worthseeing.insert_one(doc)

    return jsonify({'msg': '등록 완료'})

# 코멘트 html 보여주기
@app.route("/comment", methods=["GET"])
def comment_get():
    all_comments = list(db.worthseeing.find({}, {'_id': False}))
    return jsonify({'comments': all_comments})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
