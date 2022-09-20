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
        'title':title,
        'image':image,
        'comment':comment_receive
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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)