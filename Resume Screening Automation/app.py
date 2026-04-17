from flask import Flask, render_template, request

from resume_screening import match_resume_to_job

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    job_text = ''
    resume_text = ''

    if request.method == 'POST':
        job_text = request.form.get('job_text', '').strip()
        resume_text = request.form.get('resume_text', '').strip()
        if job_text and resume_text:
            result = match_resume_to_job(job_text, resume_text)

    return render_template(
        'index.html',
        result=result,
        job_text=job_text,
        resume_text=resume_text,
    )


if __name__ == '__main__':
    app.run(debug=True)
