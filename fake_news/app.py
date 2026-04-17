from flask import Flask, render_template, request

from news_detector import (
    NEWS_ITEMS,
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


def build_news_model(mode: str):
    corpus = [process_text(text, mode) for _, text in NEWS_ITEMS]
    labels = [label for label, _ in NEWS_ITEMS]
    vocabulary = build_vocabulary(corpus, min_freq=1)
    feature_matrix = vectorize(corpus, vocabulary)
    model = train_naive_bayes(feature_matrix, labels)
    return model, vocabulary


MODELS = {mode: build_news_model(mode) for mode in MODEL_MODES}


def classify_news(text: str, mode: str) -> tuple[str, list[str]]:
    model, vocabulary = MODELS[mode]
    tokens = process_text(text, mode)
    vector = vectorize([tokens], vocabulary)[0]
    prediction = predict_naive_bayes(model, [vector])[0]
    label = 'Fake News' if prediction == 1 else 'Real News'
    return label, tokens


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    news_text = ''
    selected_mode = 'stem'

    if request.method == 'POST':
        news_text = request.form.get('news_text', '').strip()
        selected_mode = request.form.get('mode', 'stem')
        if news_text:
            label, tokens = classify_news(news_text, selected_mode)
            result = {
                'label': label,
                'tokens': tokens,
                'mode': MODEL_MODES[selected_mode],
            }

    return render_template(
        'index.html',
        result=result,
        news_text=news_text,
        selected_mode=selected_mode,
        modes=MODEL_MODES,
    )


if __name__ == '__main__':
    app.run(debug=True)
