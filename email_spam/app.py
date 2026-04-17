from flask import Flask, render_template, request

from spam_detector import (
    EMAILS,
    process_text,
    tokenize,
    build_vocabulary,
    vectorize,
    train_naive_bayes,
    predict_naive_bayes,
)

app = Flask(__name__)

MODEL_MODES = {
    'stem': 'Stemming',
    'lemma': 'Lemmatization',
}


def build_spam_model(mode: str):
    corpus = [process_text(text, mode) for _, text in EMAILS]
    labels = [label for label, _ in EMAILS]
    vocabulary = build_vocabulary(corpus, min_freq=1)
    feature_matrix = vectorize(corpus, vocabulary)
    model = train_naive_bayes(feature_matrix, labels)
    return model, vocabulary


MODELS = {mode: build_spam_model(mode) for mode in MODEL_MODES}


def classify_email(text: str, mode: str) -> tuple[str, list[str]]:
    model, vocabulary = MODELS[mode]
    tokens = process_text(text, mode)
    vector = vectorize([tokens], vocabulary)[0]
    prediction = predict_naive_bayes(model, [vector])[0]
    label = 'Spam' if prediction == 1 else 'Not Spam'
    return label, tokens


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    email_text = ''
    selected_mode = 'stem'

    if request.method == 'POST':
        email_text = request.form.get('email_text', '').strip()
        selected_mode = request.form.get('mode', 'stem')
        if email_text:
            label, tokens = classify_email(email_text, selected_mode)
            result = {
                'label': label,
                'tokens': tokens,
                'mode': MODEL_MODES[selected_mode],
            }

    return render_template(
        'index.html',
        result=result,
        email_text=email_text,
        selected_mode=selected_mode,
        modes=MODEL_MODES,
    )


if __name__ == '__main__':
    app.run(debug=True)
