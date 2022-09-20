#flask, pymongo, dnspython,requests, bs4 일단 이렇게만 했습니다.
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

# 일단 각자 파이몽고 사용해보기! 본인 디비 주소로 바꾸세요!
from pymongo import MongoClient
client = MongoClient('mongodb+srv://password:sparta@cluster0.kythmsg.mongodb.net/?retryWrites=true&w=majority')
db = client.worth_seeing


# HTML 화면 보여주기
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/comment')
def comment():
    return render_template('comment.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)