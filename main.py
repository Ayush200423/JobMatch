from flask import Flask, redirect, url_for, render_template, request, session
import json
from mail import Mailer

from secret_key import key
from storage import StorageManager
from database.users_database import UsersDatabase
from resume_scraper import ResumeParser
from job_similarity import Similarity
from mail import Mailer

app = Flask(__name__)
app.secret_key = key

@app.route("/", methods=["GET", "POST"])
@app.route("/home/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            if users_db.read_user(email=email, password=password, auth=True):
                session['email'] = email
                return redirect(url_for('upload'))
            else:
                return render_template('home.html')
        except:
            try:
                users_db.create_user(email=email, password=password)
            except:
                return render_template('home.html')
            else:
                mailer.setup_email(user_email = email)
                mailer.send_email()
                session['email'] = email
                return redirect(url_for("upload"))
    else:
        return render_template('home.html')

@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        resume = request.files['resume-file']
        resume_parser.pdf_to_txt(resume)
        ents_dict = resume_parser.find_ents()
        users_db.update_user(email=session['email'], ents_dict=ents_dict)
        if resume.filename != '':
            session['filename'] = resume.filename
            resume_storage.insert_resume(resume = resume)
            return redirect(url_for("edit"))
        else:
            return redirect(request.url)
    else:
        if "email" in session:
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
        users_db.update_user(email=session['email'], selected_jobs=session['selected links'])
        return redirect(url_for('submit'))
    else:
        if "filename" in session:
            return render_template("results.html")
        else:
            return redirect(url_for("edit"))

@app.route("/submit/", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        return redirect(url_for("logout"))
    else:
        if 'selected links' in session:
            return render_template('submitted.html')
        else:
            return redirect(url_for('results'))

@app.route("/logout/")
def logout():
    [session.pop(key) for key in list(session.keys())]
    return redirect(url_for("home"))

# <--- /api/ endpoints --->

@app.route("/api/fetch-ents", methods=["GET"])
def fetch_ents():
    accepted_columns = ['fname', 'lname', 'phone', 'degree', 'skills', 'role', 'location']
    data = users_db.read_user(email=session['email'], auth=False)
    filtered_data = {key: value for key, value in data.items() if key in accepted_columns}
    return json.dumps(filtered_data)

@app.route("/api/upload-resume-data", methods=["POST"])
def upload_resume_data():
    res = request.get_json()
    users_db.update_user(email=session['email'], ents_dict=res)
    return res

@app.route("/api/fetch-relevant-postings", methods=["GET"])
def fetch_relevant_postings():
    all_jobs = {}
    data = users_db.read_user(session['email'], auth=False)
    role = data['role']
    location = data['location']
    skills = data['skills']
    certifications = data['degree']
    job_sim = Similarity(role = role, location = location, resume_data = f"{skills} {role} {certifications}")
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
    for state, links in res.items():
        if state == 'append':
            for link in links:
                selected_links.append(link)
        else:
            for link in links:
                selected_links.remove(link)
    session['selected links'] = selected_links
    return res

if __name__ == '__main__':
    resume_storage = StorageManager()
    resume_parser = ResumeParser()
    users_db = UsersDatabase()
    mailer = Mailer()
    app.run()