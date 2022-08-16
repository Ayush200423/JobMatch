import email
from flask import Flask, redirect, url_for, render_template, request, session
import requests
import tempfile
import json

from secret_key import key
from storage import StorageManager
from resume_scraper import ResumeParser
from job_similarity import Similarity
from auto_apply import AutoApply

app = Flask(__name__)
app.secret_key = key

def named_temp_file(url = None, **user_info):
    resume_url = resume_storage.get_resume_url(filename = session['filename'])
    get_resume = requests.get(resume_url)
    if url:
        auto_apply.open_url_iframe(url=url)
        auto_apply.fill_personal_info(user_info['email'], user_info['password'], user_info['fname'], user_info['lname'], user_info['phone'], user_info['jobtitle'], user_info['location'])
        with tempfile.NamedTemporaryFile(dir='./active_files', suffix='.pdf') as tmp_file:
            tmp_file.write(get_resume.content)
            tmp_file_path = tmp_file.name
            auto_apply.fill_work(tmp_file_path)
            return
    else:
        with tempfile.NamedTemporaryFile(dir='./active_files', suffix='.pdf') as tmp_file:
            tmp_file.write(get_resume.content)
            tmp_file_path = tmp_file.name
            resume_parser.pdf_to_txt(tmp_file_path)
            ents_dict = resume_parser.find_ents()
        for label, ents in ents_dict.items():
            if ents_dict[label] != '':
                session[label.lower()] = ents
        return ents_dict

@app.route("/", methods=["GET", "POST"])
@app.route("/home/", methods=["GET", "POST"])
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
        return redirect(url_for("results"))
    else:
        if "filename" in session:
            return render_template("edit-details.html")
        else:
            return redirect(url_for("upload"))

@app.route("/results/", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        email = session['email']
        password = session['password']
        fname = session['fname']
        lname = session['lname']
        phone = session['phone']
        jobtitle = session['role']
        location = session['location']
        for url in session['selected links']:
            named_temp_file(url=url, email=email, password=password, fname=fname, lname=lname, phone=phone, jobtitle=jobtitle, location=location)
    else:
        if "skills" in session:
            return render_template("results.html")
        else:
            return redirect(url_for("edit-details"))

# <--- /api/ --->

@app.route("/api/fetch-ents", methods=["GET"])
def fetch_ents():
    return json.dumps(named_temp_file())

@app.route("/api/upload-resume-data", methods=["POST"])
def upload_resume_data():
    res = request.get_json()
    for key, value in res.items():
        session[key] = value
    return res

@app.route("/api/fetch-relevant-postings", methods=["GET"])
def fetch_relevant_postings():
    all_jobs = {}
    job_sim = Similarity(role = session['role'], location = session['location'], resume_data = f"{session['skills']} {session['role']}")
    jobs = job_sim.get_jobs()
    for job_index in range(len(jobs)):
        posting, confidence = jobs[job_index]
        posting['confidence'] = confidence
        all_jobs[f'job{job_index}'] = posting
    return json.dumps(all_jobs)

@app.route("/api/upload-checkbox-state", methods=["POST"])
def upload_checkbox_state():
    res = request.get_json()
    try:
        selected_links = session['selected links']
    except:
        selected_links = []
    for state, link in res.items():
        if state == 'append':
            selected_links.append(link)
        else:
            selected_links.remove(link)
    session['selected links'] = selected_links
    return res

# <--- /logout/ --->

@app.route("/logout/")
def logout():
    [session.pop(key) for key in list(session.keys())]
    return redirect(url_for("home"))

if __name__ == '__main__':
    resume_storage = StorageManager()
    resume_parser = ResumeParser()
    auto_apply = AutoApply()
    app.run(debug = True)