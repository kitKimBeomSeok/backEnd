import os


import requests
from flask import Flask, render_template, redirect, request, session, url_for
from servcie import music_service,musicPlaylist_service,user_service,sheets_service,playplist_service
from sqlalchemy import create_engine
from sqlite3 import IntegrityError
import orm_models.table
from orm_models.table import Music, User, Playlist, MusicPlaylist,Sheet
from sqlalchemy.orm import sessionmaker

# 데이터베이스 연결 엔진 생성
engine = create_engine('mysql+pymysql://root:102302@127.0.0.1/music', echo=True)
# Session 클래스 생성
Session = sessionmaker(bind=engine)
# Session 인스턴스 생성
DB_session = Session()


app = Flask(__name__)
app.secret_key = os.urandom(24)
user_id = ""
client_id = "76ad3ecef7e03503b0871a190cd6a3e0"
redirect_uri = "http://localhost/redirect"
kauth_host = "https://kauth.kakao.com"
kapi_host = "https://kapi.kakao.com"
client_secret = "h1trrHlAnzG6IKCGFs5PcoSIOelrmWDq"


@app.route("/")
def home():
    return render_template('ATM_Build/index.html')


@app.route("/authorize")
def authorize():
    print(123)
    scope_param = ""
    if request.args.get("scope"):
        scope_param = "&scope=" + request.args.get("scope")


    return redirect(
        "{0}/oauth/authorize?response_type=code&client_id={1}&redirect_uri={2}{3}".format(kauth_host, client_id,
                                                                                          redirect_uri, scope_param))


@app.route("/redirect")
def redirect_page():
    print(456)
    data = {'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'client_secret': client_secret,
            'code': request.args.get("code")}

    resp = requests.post(kauth_host + "/oauth/token", data=data)
    session['access_token'] = resp.json()['access_token']
    print(session)
    headers = {'Authorization': 'Bearer ' + session['access_token'],
               'Content-type': 'Content-type: application/x-www-form-urlencoded;charset=utf-8'}
    temp = requests.get(kapi_host + "/v2/user/me", headers=headers)

    data = temp.json()
    #session에 사용자정보 추가
    session['user_id'] = data['id']
    session['user_name'] = data['properties']['nickname']

    #새로운 사용자 추가
    try:
        DB_session = Session()
        user_id = session['user_id']
        user_name = session['user_name']
        user_service.create_user(DB_session, user_id,user_name)
    finally:
        # Session 종료
        DB_session.close()
    return redirect("/")


@app.route("/profile")
def profile():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    resp = requests.get(kapi_host + "/v2/user/me", headers=headers)
    print(resp)
    print(session.get('user_id'))
    return resp.text


@app.route("/friends")
def friends():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    resp = requests.get(kapi_host + "/v1/api/talk/friends", headers=headers)
    return resp.text



@app.route("/message")
def message():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    data = {
        'template_object': '{"object_type":"text","text":"Hello, world!","link":{"web_url":"https://developers.kakao.com","mobile_web_url":"https://developers.kakao.com"}}'}
    resp = requests.post(kapi_host + "/v2/api/talk/memo/default/send", headers=headers, data=data)
    return resp.text


@app.route("/friends_message")
def friends_message():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    data = {
        'receiver_uuids': '[{0}]'.format(request.args.get("uuids")),
        'template_object': '{"object_type":"text","text":"Hello, world!","link":{"web_url":"https://developers.kakao.com","mobile_web_url":"https://developers.kakao.com"}}'}
    resp = requests.post(kapi_host + "/v1/api/talk/friends/message/default/send", headers=headers, data=data)
    return resp.text


@app.route("/logout")
def logout():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    print("fuck")
    resp = requests.post(kapi_host + "/v1/user/logout", headers=headers)
    session.clear()  # 세션 초기화
    return resp.text

@app.route("/leave")
def leave():
    #회원 탈퇴에 따른 사용자 삭제
    try:
        DB_session = Session()
        user_id = session['user_id']
        user_name = session['user_name']
        user_service.delete_user(DB_session, user_id, user_name)
    finally:
        # Session 종료
        DB_session.close()

    headers = {'Authorization': 'Bearer ' + session['access_token']}
    resp = requests.post(kapi_host + "/v1/user/unlink", headers=headers)
    session.clear()  # 세션 초기화
    return resp.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)