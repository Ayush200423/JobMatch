from crypt import methods
from flask import Flask, redirect, url_for, render_template, request, session
import requests
import tempfile
import json

from secret_key import key
from storage import StorageManager
from resume_scraper import ResumeParser
from auto_apply import AutoApply

app = Flask(__name__)
app.secret_key = key

def named_temp_file(url = None, auto_apply = False):
    resume_url = resume_storage.get_resume_url(filename = session['filename'])
    get_resume = requests.get(resume_url)
    if auto_apply:
        email = session['email']
        password = session['password']
        with tempfile.NamedTemporaryFile(dir='./active_files', suffix='.pdf') as tmp_file:
            tmp_file.write(get_resume.content)
            tmp_file_path = tmp_file.name
            application_bot = AutoApply(email=email, password=password, firstname='MOO', surname='yess', phone=20324813, resume_path=tmp_file_path, jobtitle='Software Engineer', location='Toronto, ON')
            application_bot.apply(url)
    else:
        with tempfile.NamedTemporaryFile(dir='./active_files', suffix='.pdf') as tmp_file:
            tmp_file.write(get_resume.content)
            tmp_file_path = tmp_file.name
            resume_parser.pdf_to_txt(tmp_file_path)
            ents_dict = resume_parser.find_ents()
        for label, ents in ents_dict.items():
            session[label.lower()] = ' '.join(ents)
        return ents_dict
    return

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        session['password'] = password
        return redirect(url_for("upload"))
    else:
        if "email" in session and "password" in session:
            return redirect(url_for("upload"))
        else:
            return render_template('home.html')

@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        resume = request.files['resume-file']
        if resume.filename != '':
            session['filename'] = resume.filename
            resume_storage.insert_resume(resume = resume)
            return redirect(url_for("edit"))
        else:
            return redirect(request.url)
    else:
        if "email" in session and "password" in session:
            return render_template("upload.html")
        else:
            return redirect(url_for("home"))

@app.route("/edit/", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        pass
    else:
        return render_template("edit_details.html")

@app.route("/fetchents", methods=["GET"])
def fetchents():
    return json.dumps(named_temp_file())

@app.route("/logout/")
def logout():
    [session.pop(key) for key in list(session.keys())]
    return redirect(url_for("home"))

if __name__ == '__main__':
    resume_storage = StorageManager()
    resume_parser = ResumeParser()
    app.run(debug = True)