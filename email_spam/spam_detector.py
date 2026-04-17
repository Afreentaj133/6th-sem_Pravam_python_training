import math
import random
import re
from collections import Counter, defaultdict

STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'could', 'did', 'do',
    'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having',
    'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is',
    'it', 'its', 'itself', 'let', 'me', 'more', 'most', 'my', 'myself', 'nor', 'of', 'off', 'on', 'once', 'only',
    'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so', 'some',
    'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they',
    'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what',
    'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself',
    'yourselves'
}

EMAILS = [
    (1, "<html><body>Congratulations! You have won a $1000 gift card. Claim now!</body></html>"),
    (1, "Earn money from home fast with our proven system. Limited time offer."),
    (1, "Get cheap meds online without prescription. Buy now and save big!"),
    (1, "You have been selected for a free vacation to Bahamas. Click this link."),
    (1, "Immediate response required: update your account details to avoid closure."),
    (1, "Hot singles are waiting for you. Start chatting instantly."),
    (1, "This is not spam. Open immediately and get rich quick investments."),
    (1, "Winner! You are chosen for a prize. Send your details to collect."),
    (1, "Urgent: Your payment was declined. Verify your payment information."),
    (1, "Act now to receive a free iPhone. Offer expires tonight."),
    (0, "Hi team, the meeting is rescheduled to Monday at 10 AM. Please confirm."),
    (0, "Please find the attached report and let me know your feedback."),
    (0, "Lunch tomorrow? I can meet after 1 PM at the campus cafe."),
    (0, "Your appointment with Dr. Patel is set for Tuesday at 3:30 PM."),
    (0, "The quarterly sales figures are attached. Review before the next call."),
    (0, "Can you share the editable version of the presentation by tonight?"),
    (0, "Family reunion this weekend at my place. Bring snacks and drinks."),
    (0, "Here is the code snippet from today’s discussion. Let me know if it helps."),
    (0, "Your invoice is attached. Please process the payment within 30 days."),
    (0, "Thanks for your help with the project. I appreciated the quick turnaround."),
]


def clean_text(text: str) -> str:
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'http\S+|www\.[^\s]+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text: str) -> list[str]:
    return [token for token in text.split() if token]


def remove_stop_words(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in STOP_WORDS]


def simple_stem(token: str) -> str:
    if len(token) <= 3:
        return token
    if token.endswith('ies'):
        return token[:-3] + 'y'
    if token.endswith('sses') or token.endswith('shes') or token.endswith('ches'):
        return token[:-2]
    if token.endswith('s') and not token.endswith('ss'):
        return token[:-1]
    if token.endswith('ing') and len(token) > 5:
        return token[:-3]
    if token.endswith('ed') and len(token) > 4:
        return token[:-2]
    return token


def simple_lemmatize(token: str) -> str:
    lemma_map = {
        'went': 'go', 'gone': 'go', 'bought': 'buy', 'brought': 'bring', 'sent': 'send',
        'received': 'receive', 'running': 'run', 'meeting': 'meet', 'paid': 'pay', 'using': 'use',
    }
    if token in lemma_map:
        return lemma_map[token]
    if token.endswith('ies') and len(token) > 4:
        return token[:-3] + 'y'
    if token.endswith('ves') and len(token) > 4:
        return token[:-3] + 'f'
    if token.endswith('ing') and len(token) > 5:
        return token[:-3]
    if token.endswith('ed') and len(token) > 4:
        base = token[:-2]
        if base.endswith('i'):
            return base[:-1] + 'y'
        return base
    if token.endswith('s') and len(token) > 3:
        return token[:-1]
    return token


def process_text(text: str, stem_or_lemma: str) -> list[str]:
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stop_words(tokens)
    if stem_or_lemma == 'stem':
        return [simple_stem(token) for token in tokens]
    if stem_or_lemma == 'lemma':
        return [simple_lemmatize(token) for token in tokens]
    return tokens


def build_vocabulary(corpus: list[list[str]], min_freq: int = 1) -> dict[str, int]:
    freq = Counter(token for tokens in corpus for token in tokens)
    vocabulary = {token: idx for idx, (token, count) in enumerate(sorted(freq.items())) if count >= min_freq}
    return vocabulary


def vectorize(corpus: list[list[str]], vocabulary: dict[str, int]) -> list[list[int]]:
    vectors = []
    for tokens in corpus:
        vector = [0] * len(vocabulary)
        counts = Counter(tokens)
        for token, count in counts.items():
            if token in vocabulary:
                vector[vocabulary[token]] = count
        vectors.append(vector)
    return vectors


def train_naive_bayes(X: list[list[int]], y: list[int], alpha: float = 1.0) -> dict:
    class_counts = Counter(y)
    feature_counts = {label: [0] * len(X[0]) for label in class_counts}
    total_tokens = {label: 0 for label in class_counts}

    for vector, label in zip(X, y):
        for idx, count in enumerate(vector):
            feature_counts[label][idx] += count
            total_tokens[label] += count

    vocab_size = len(X[0])
    model = {
        'priors': {label: class_counts[label] / len(y) for label in class_counts},
        'cond_prob': {},
    }

    for label in class_counts:
        model['cond_prob'][label] = [
            (feature_counts[label][idx] + alpha) / (total_tokens[label] + alpha * vocab_size)
            for idx in range(vocab_size)
        ]

    return model


def predict_naive_bayes(model: dict, X: list[list[int]]) -> list[int]:
    predictions = []
    for vector in X:
        scores = {}
        for label, prior in model['priors'].items():
            score = math.log(prior)
            for idx, count in enumerate(vector):
                if count > 0:
                    score += count * math.log(model['cond_prob'][label][idx])
            scores[label] = score
        predictions.append(max(scores, key=scores.get))
    return predictions


def accuracy_score(true: list[int], pred: list[int]) -> float:
    return sum(1 for a, b in zip(true, pred) if a == b) / len(true)


def classification_report(true: list[int], pred: list[int]) -> dict[str, float]:
    tp = sum(1 for t, p in zip(true, pred) if t == 1 and p == 1)
    tn = sum(1 for t, p in zip(true, pred) if t == 0 and p == 0)
    fp = sum(1 for t, p in zip(true, pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(true, pred) if t == 1 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        'accuracy': accuracy_score(true, pred),
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def split_dataset(data: list[tuple[int, str]], test_ratio: float = 0.3, seed: int = 42):
    random.seed(seed)
    data_copy = data.copy()
    random.shuffle(data_copy)
    split = int(len(data_copy) * (1 - test_ratio))
    train, test = data_copy[:split], data_copy[split:]
    return train, test


def run_pipeline(mode: str) -> dict:
    train_data, test_data = split_dataset(EMAILS)

    train_texts = [' '.join(process_text(text, mode)) for _, text in train_data]
    test_texts = [' '.join(process_text(text, mode)) for _, text in test_data]
    y_train = [label for label, _ in train_data]
    y_test = [label for label, _ in test_data]

    corpus = [tokenize(text) for text in train_texts]
    vocabulary = build_vocabulary(corpus, min_freq=1)
    X_train = vectorize(corpus, vocabulary)
    X_test = vectorize([tokenize(text) for text in test_texts], vocabulary)

    model = train_naive_bayes(X_train, y_train)
    predictions = predict_naive_bayes(model, X_test)
    report = classification_report(y_test, predictions)

    return {
        'mode': mode,
        'vocab_size': len(vocabulary),
        'model': model,
        'report': report,
        'test_texts': test_texts,
        'predictions': predictions,
        'y_test': y_test,
    }


def print_results(results: dict) -> None:
    print(f"=== {results['mode'].upper()} RESULTS ===")
    print(f"Vocabulary size: {results['vocab_size']}")
    print('Metrics:')
    for name, value in results['report'].items():
        print(f"  {name.capitalize()}: {value:.2f}")
    print('\nSample predictions:')
    for text, pred, truth in zip(results['test_texts'], results['predictions'], results['y_test']):
        label = 'SPAM' if pred == 1 else 'HAM'
        actual = 'SPAM' if truth == 1 else 'HAM'
        print(f"  [{actual}] predicted={label}: {text}")
    print('\n')


def compare_stemming_and_lemmatization():
    for mode in ['stem', 'lemma']:
        results = run_pipeline(mode)
        print_results(results)


if __name__ == '__main__':
    import math

    compare_stemming_and_lemmatization()
