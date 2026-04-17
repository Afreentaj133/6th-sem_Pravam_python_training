from flask import Flask, render_template, request

from answer_evaluation import evaluate_answer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    reference_text = ''
    student_text = ''

    if request.method == 'POST':
        reference_text = request.form.get('reference_text', '').strip()
        student_text = request.form.get('student_text', '').strip()
        if reference_text and student_text:
            result = evaluate_answer(reference_text, student_text)

    return render_template(
        'index.html',
        result=result,
        reference_text=reference_text,
        student_text=student_text,
    )


if __name__ == '__main__':
    app.run(debug=True)
