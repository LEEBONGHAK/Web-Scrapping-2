from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file


# 웹사이트 만들기
app = Flask("Super Scrapper")  # 이름 지정 및 생성


# 더 빠른 scrapper를 위해 가짜 DB를 생성
db = {}


# @(데코레이터) : 바로 아래의 '함수'를 찾아 실행
@app.route("/") # 누군가가 "/"에 접속하면 웹사이트의 route에 접속 가능
def home():
  return render_template("home.html")

# # url이랑 주고받고 하기
# @app.route("/contact")
# def contact():
#   return "Contact me!"


# Dynamic URL
@app.route("/<username>")
# <> : placeholder
def username(username):
  return f"Hello {username} how are you doing"

@app.route("/report")
def report():
  word = request.args.get("word")
  # request를 통해 원하는 데이터 추출

  if word:
    word=word.lower()
    existing_jobs = db.get(word)
    
    if existing_jobs:
      jobs = existing_jobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/") # home으로 다시 이동

  return render_template("report.html", searching_by=word, result_nums=len(jobs), jobs=jobs)


# 파이썬 코드를 html에서 친다면(flask), {%%}안에 쳐 줘야함
@app.route("/export")
def export():
  try:
    word = request.args.get("word")

    if not word:
      raise Exception()

    word = word.lower()
    jobs = db.get(word)

    if not jobs:
      raise Exception()

    save_to_file(jobs)

    return send_file("jobs.csv", mimetype='application/x-csv', attachment_filename='summary_report.csv', as_attachment=True)
  except:
    return redirect("/")



# host="0.0.0.0" : repl.it에서 공개하는 웹사이트 생성 - 서버를 구축한 셈
# app.run(host="0.0.0.0")

# repl 말고 로컬에서는 웹페이지가 0.0.0.0 은 안됨, 127.0.0.1 로 지정
app.run(host="127.0.0.1")